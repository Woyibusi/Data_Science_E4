import numpy as np
import pandas as pd
from pmdarima import auto_arima
import joblib
from pathlib import Path
import os
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import acorr_ljungbox
import json
from sklearn.metrics import mean_absolute_error, mean_squared_error
from app.data import data_loader, preprocess
import warnings

warnings.filterwarnings("ignore")

def train_model(series, test_series=None, save_dir='models'):
    """Entraîne un modèle ARIMA automatique et évalue ses performances."""
    data = series.values
    print("Entraînement ARIMA Automatique en cours...")
    
    # Train ARIMA model with auto_arima
    model = auto_arima(
        data,
        start_p=1, start_q=1,
        max_p=5, max_q=5,
        d=None,
        seasonal=False,
        trace=True,
        error_action='ignore',
        suppress_warnings=True,
        stepwise=True
    )
    model_name = "ARIMA_Automatique"
    print(model.summary())
    
    # In-sample predictions (fitted values)
    fitted = model.predict_in_sample()
    residuals = data - fitted
    
    # Calcul des métriques avec gestion robuste de acorr_ljungbox
    lb_result = acorr_ljungbox(residuals, lags=[10], return_df=False)
    if isinstance(lb_result, tuple):
        p_value = float(lb_result[1][0])  # Anciennes versions de statsmodels
    else:
        p_value = float(lb_result['lb_pvalue'].iloc[0])  # Versions récentes
    metrics = {
        'AIC': float(model.aic()),
        'Ljung-Box p-value (lag 10)': p_value
    }
    
    # Out-of-sample evaluation if test_series provided
    if test_series is not None:
        test_data = test_series.values
        test_preds = model.predict(n_periods=len(test_data))
        metrics['MAE'] = mean_absolute_error(test_data, test_preds)
        metrics['RMSE'] = np.sqrt(mean_squared_error(test_data, test_preds))
        metrics['MAPE'] = np.mean(np.abs((test_data - test_preds) / test_data)) * 100
    
    # Print evaluation
    print("\nÉvaluation pendant l'entraînement:")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")
    if metrics['Ljung-Box p-value (lag 10)'] > 0.05:
        print("Résidus semblent non corrélés (bon signe)")
    else:
        print("Résidus montrent une corrélation (ajustement peut être amélioré)")
    
    # Plot training results
    os.makedirs(save_dir, exist_ok=True)
    
    # Plot 1: Fitted vs Actual
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(series.index, data, label='Données Réelles', color='blue')
    plt.plot(series.index, fitted, label='Valeurs Ajustées', color='red', linestyle='--')
    plt.title(f'Entraînement {model_name} (AIC: {metrics["AIC"]:.2f})')
    plt.xlabel('Date')
    plt.ylabel('Valeur')
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Residuals ACF
    plt.subplot(2, 1, 2)
    plot_acf(residuals, ax=plt.gca(), lags=20)
    plt.title('ACF des Résidus')
    
    plt.tight_layout()
    plot_file = Path(save_dir) / f'{model_name}_training_plots.png'
    plt.savefig(plot_file)
    plt.close()
    print(f"Graphiques d'entraînement sauvegardés sous {plot_file}")
    
    # Save metrics to JSON
    metrics_file = Path(save_dir) / f'{model_name}_metrics.json'
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(f"Métriques sauvegardées sous {metrics_file}")
    
    # Save the trained model
    model_file = Path(save_dir) / f'{model_name}.joblib'
    joblib.dump(model, model_file)
    print(f"Modèle sauvegardé sous {model_file}")
    
    return model

def forecast_model(model, steps=96):
    """Génère des prédictions pour un nombre donné de pas."""
    return model.predict(n_periods=steps)

if __name__ == "__main__":
    # Load data once at startup
    series = data_loader.load_consumption_data("/Users/macos/Desktop/Data_Sciences/Data_Science_E4/app/data")
    series = preprocess.clean_series(series)
    
    # Split data into train/test
    split_idx = int(0.8 * len(series))
    train_data = series.iloc[:split_idx]
    test_data = series.iloc[split_idx:]
    
    # Train with test set for full evaluation
    arima_model = train_model(train_data, test_series=test_data)
    preds = forecast_model(arima_model, steps=5)
    print("Prédictions ARIMA:", preds)
    
    # Load saved metrics for reuse
    with open('models/ARIMA_Automatique_metrics.json', 'r') as f:
        saved_metrics = json.load(f)
    print("Métriques chargées:", saved_metrics)
