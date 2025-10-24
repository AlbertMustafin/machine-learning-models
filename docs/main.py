import os
import logging
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import pandas as pd

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Load data
        data = pd.read_csv('data.csv')
        logger.info('Data loaded successfully')

        # Split data into features and target
        X = data.drop('target', axis=1)
        y = data['target']

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale data
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Build model
        model = Sequential()
        model.add(Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Train model
        model.fit(X_train_scaled, y_train, epochs=10, batch_size=128, verbose=0)

        # Evaluate model
        y_pred = model.predict(X_test_scaled)
        y_pred_class = (y_pred > 0.5).astype('int32')
        accuracy = accuracy_score(y_test, y_pred_class)
        logger.info(f'Model accuracy: {accuracy:.2f}')

        # Save model
        model.save('model.h5')
        logger.info('Model saved successfully')

    except Exception as e:
        logger.error(f'Error: {e}')
        exit(1)