"""
LSTM model architecture for stock price prediction.
"""
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam


def create_lstm_model(lookback_window: int = 60, features: int = 1) -> Sequential:
    """Create LSTM model architecture for stock price prediction.
    
    Args:
        lookback_window: Number of previous days to use for prediction (default: 60)
        features: Number of features in input data (default: 1 for closing price)
    
    Returns:
        Compiled Keras Sequential model
    """
    model = Sequential([
        # First LSTM layer with dropout for regularization
        LSTM(units=50, return_sequences=True, input_shape=(lookback_window, features)),
        Dropout(0.2),
        
        # Second LSTM layer
        LSTM(units=50, return_sequences=True),
        Dropout(0.2),
        
        # Third LSTM layer
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        
        # Dense layers
        Dense(units=25),
        Dense(units=1)
    ])
    
    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='mean_squared_error',
        metrics=['mae']
    )
    
    return model


def train_model(model: Sequential, X_train: np.ndarray, y_train: np.ndarray, 
                epochs: int = 50, batch_size: int = 32, validation_split: float = 0.1):
    """Train the LSTM model.
    
    Args:
        model: Keras model to train
        X_train: Training features
        y_train: Training labels
        epochs: Number of training epochs
        batch_size: Batch size for training
        validation_split: Fraction of data to use for validation
    
    Returns:
        Training history
    """
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=validation_split,
        verbose=0,
        shuffle=False  # Don't shuffle time series data
    )
    
    return history
