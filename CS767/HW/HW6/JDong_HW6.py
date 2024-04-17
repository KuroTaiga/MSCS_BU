import numpy as np
import keras
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from minisom import MiniSom
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras import layers, models
import time

# Step 1: Load and preprocess the Fashion-MNIST dataset
(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
X_train = X_train.reshape(X_train.shape[0], -1).astype('float32') / 255.0
X_test = X_test.reshape(X_test.shape[0], -1).astype('float32') / 255.0

# Normalize pixel values
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


(x_train, _), (x_test, _) = fashion_mnist.load_data()
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = np.expand_dims(x_train,-1)
x_test = np.expand_dims(x_test,-1)
# Step 2: Dimensionality Reduction
# SOM
def do_SOM(X_train_scaled):
    print("Starting SOM")
    som = MiniSom(7, 7, X_train_scaled.shape[1], sigma=0.3, learning_rate=0.5)
    som.random_weights_init(X_train_scaled)
    som.train_random(X_train_scaled, 100)
    som_train = np.array([som.winner(x) for x in X_train_scaled])
    return som,som_train

som, som_train = do_SOM(X_train_scaled)

# RBM

def do_rbm(X_train_scaled):
    print("Starting RBM")
    rbm = BernoulliRBM(random_state=19970107, verbose=True)
    rbm_pipeline = Pipeline(steps=[('rbm', rbm), ('pca', PCA(n_components=50))])
    rbm_pipeline.fit(X_train_scaled)
    rbm_train = rbm_pipeline.transform(X_train_scaled)
    return rbm_pipeline,rbm_train

rbm_pipeline, rbm_train = do_rbm(X_train_scaled)

# Autoencoder (VAE)
# Implement autoencoder using TensorFlow/Keras or PyTorch
# VAE architecture
latent_dim = 50  # dimensionality of the latent space

# Encoder
encoder_inputs = tf.keras.Input(shape=(28,28,1))
x = layers.Dense(256, activation='relu')(encoder_inputs)
z_mean = layers.Dense(latent_dim, name='z_mean')(x)
z_log_var = layers.Dense(latent_dim, name='z_log_var')(x)

# Reparameterization trick to sample from latent space
class Sampling(layers.Layer):
    """Uses (z_mean, z_log_var) to sample z, the vector encoding a digit."""

    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon
# ----- Building Encoder and decoder -------
latent_dim = 2

encoder_inputs = keras.Input(shape=(28,28, 1)) #28*28
x = layers.Conv2D(32, 3, activation="relu", strides=2, padding="same")(encoder_inputs)
x = layers.Conv2D(64, 3, activation="relu", strides=2, padding="same")(x)
x = layers.Flatten()(x)
x = layers.Dense(16, activation="relu")(x)
z_mean = layers.Dense(latent_dim, name="z_mean")(x)
z_log_var = layers.Dense(latent_dim, name="z_log_var")(x)
z = Sampling()([z_mean, z_log_var])
encoder = keras.Model(encoder_inputs, [z_mean, z_log_var, z], name="encoder")
#encoder.summary()

latent_inputs = keras.Input(shape=(latent_dim,))
x = layers.Dense(7 * 7 * 64, activation="relu")(latent_inputs)
x = layers.Reshape((7, 7, 64))(x)
x = layers.Conv2DTranspose(64, 3, activation="relu", strides=2, padding="same")(x)
x = layers.Conv2DTranspose(32, 3, activation="relu", strides=2, padding="same")(x)
decoder_outputs = layers.Conv2DTranspose(1, 3, activation="sigmoid", padding="same")(x)
decoder = keras.Model(latent_inputs, decoder_outputs, name="decoder")
#decoder.summary()
class VAE(keras.Model):
    def __init__(self, encoder, decoder, **kwargs):
        super(VAE, self).__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
        self.total_loss_tracker = keras.metrics.Mean(name="total_loss")
        self.reconstruction_loss_tracker = keras.metrics.Mean(
            name="reconstruction_loss"
        )
        self.kl_loss_tracker = keras.metrics.Mean(name="kl_loss")

    @property
    def metrics(self):
        return [
            self.total_loss_tracker,
            self.reconstruction_loss_tracker,
            self.kl_loss_tracker,
        ]

    def train_step(self, data):
        with tf.GradientTape() as tape:
            z_mean, z_log_var, z = self.encoder(data)
            reconstruction = self.decoder(z)
            reconstruction_loss = tf.reduce_mean(
                tf.reduce_sum(
                    keras.losses.binary_crossentropy(data, reconstruction), axis=(1, 2)
                )
            )
            kl_loss = -0.5 * (1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
            kl_loss = tf.reduce_mean(tf.reduce_sum(kl_loss, axis=1))
            total_loss = reconstruction_loss + kl_loss
        grads = tape.gradient(total_loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))
        self.total_loss_tracker.update_state(total_loss)
        self.reconstruction_loss_tracker.update_state(reconstruction_loss)
        self.kl_loss_tracker.update_state(kl_loss)
        return {
            "loss": self.total_loss_tracker.result(),
            "reconstruction_loss": self.reconstruction_loss_tracker.result(),
            "kl_loss": self.kl_loss_tracker.result(),
        }

# ---- Train the VAE -----------

vae = VAE(encoder, decoder)
vae.compile(optimizer=keras.optimizers.Adam())
x_vae_fit = np.concatenate([x_train, x_test], axis=0)
vae.fit(x_vae_fit, epochs=10, batch_size=128)
# Use encoder part to get reduced dimensionality representation
#using z_mean
x_train_encoded = encoder.predict(x_train)[0]
#X_train_vae = decoder.predict(x_train_encoded)
x_test_encoded = encoder.predict(x_test)[0]
#X_test_vae = decoder.predict(x_test_encoded)

# Step 3: Classifier Algorithms
classifiers = {
    "XGBoost": XGBClassifier(),
    "LightGBM": LGBMClassifier(verbose=0),
    "CATBoost": CatBoostClassifier(verbose=0)
}

datasets = {
    "Original": (X_train_scaled, X_test_scaled),
    "SOM": (som_train, np.array([som.winner(x) for x in X_test_scaled])),
    "RBM": (rbm_train, rbm_pipeline.transform(X_test_scaled)),
    # Add Autoencoder dataset here
    "VAE": (x_train_encoded, x_test_encoded)
}

results = {}

for dataset_name, (X_train_reduced, X_test_reduced) in datasets.items():
    print("Running dataset:",dataset_name)
    results[dataset_name] = {}
    for clf_name, clf in classifiers.items():
        print("    Running classifier:",clf_name)
        start_time = time.time()
        clf.fit(X_train_reduced, y_train)
        train_time = time.time() - start_time

        start_time = time.time()
        accuracy = clf.score(X_test_reduced, y_test)
        test_time = time.time() - start_time

        results[dataset_name][clf_name] = {
            "Accuracy": accuracy,
            "Training Time": train_time,
            "Test Time": test_time
        }

# Step 4: Execution Time Measurement - Already included in the loop above

# Step 5: Comparison and Reporting
for dataset_name, dataset_results in results.items():
    print(f"Results for {dataset_name}:")
    for clf_name, metrics in dataset_results.items():
        print(f"{clf_name}:")
        print(f"  Accuracy: {metrics['Accuracy']:.4f}")
        print(f"  Training Time: {metrics['Training Time']:.4f} seconds")
        print(f"  Test Time: {metrics['Test Time']:.4f} seconds")
        print()
