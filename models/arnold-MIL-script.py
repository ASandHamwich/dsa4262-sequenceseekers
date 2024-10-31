
# %%
# Libraries
import numpy as np
import tensorflow as tensorflow
from io import StringIO
import pandas as pd

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalMaxPooling1D, Masking, Input, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve, ConfusionMatrixDisplay, RocCurveDisplay, auc, precision_recall_curve

from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE, RandomOverSampler
from collections import Counter

import matplotlib.pyplot as plt


# %%

print("Loading data...")
# load numpy arrays
loaded = np.load('../data/MIL_padded_data.npz')
X_array = loaded['x']
y_vector = loaded['y']


# Grouping Information
with open('../data/data.info.labelled') as r:
    labels = r.read()

labels_df = pd.read_csv(StringIO(labels))
groups = labels_df['gene_id'].values

print("Data loaded!")

# %% [markdown]
# ## Data

# %%
print("Prepping data...")
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=21)

for train_idx, test_idx in gss.split(X_array, y_vector, groups):
    X_train, X_test = X_array[train_idx], X_array[test_idx]
    y_train, y_test = y_vector[train_idx], y_vector[test_idx]


# %%
print("Training data shape:", X_train.shape)
print("Test data shape:", X_test.shape)
print("Training labels shape:", y_train.shape)
print("Test labels shape:", y_test.shape)

# %%
print(f"Training class distribution: {Counter(y_train)}")
print(f"Test class distribution: {Counter(y_test)}")



# %% [markdown]
# Oversampling

# %%
num_bags, max_num_instances, num_features = X_train.shape
X_train_reshaped = X_train.reshape((num_bags, max_num_instances * num_features))

ros = RandomOverSampler(random_state=21)
X_train_resampled_2D, y_train = ros.fit_resample(X_train_reshaped, y_train)

num_resampled_bags = X_train_resampled_2D.shape[0]
X_train = X_train_resampled_2D.reshape((num_resampled_bags, max_num_instances, num_features))


# %%
print("X_train_resampled_final shape:", X_train.shape)
print("y_train_resampled_final shape:", y_train.shape)
print("Data prepped!")
# %%

print("Preparing model...")
model = Sequential()

input_shape = (X_train.shape[1], X_train.shape[2]) # Shape

model.add(Input(shape=input_shape))
model.add(Masking(mask_value=0.0))
model.add(Dense(64, activation='relu')) 
model.add(Dense(32, activation='relu'))

model.add(GlobalMaxPooling1D())
model.add(Dense(1, activation='sigmoid'))


# %%
model.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy', metrics=['accuracy', 'precision', 'recall', 'auc'])

# Early stopping to prevent overfitting
early_stopping = EarlyStopping(monitor='val_auc', patience=10, restore_best_weights=True)

# %%

print("Running model...")
history = model.fit(X_train, y_train, 
    validation_data=(X_test, y_test), 
    epochs=50, 
    batch_size=32, 
    callbacks=[early_stopping])

# %%
# Predict probabilities for the test set
y_pred_proba = model.predict(X_test)

# Calculate ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
auc_score = roc_auc_score(y_test, y_pred_proba)
print(f"AUC Score: {auc_score:.4f}")

# Plot the ROC curve
plt.plot(fpr, tpr, label=f"ROC curve (AUC = {auc_score:.2f})")
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc="lower right")
plt.show()

# PR-AUC
precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba)

# Compute the AUC for the precision-recall curve
pr_auc = auc(recall, precision)

# Plot the Precision-Recall curve
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, label=f'Precision-Recall AUC = {pr_auc:.2f}')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc='best')
plt.grid()
plt.show()

# Confusion matrix
y_pred_class = (y_pred_proba > 0.5).astype(int)  # Convert probabilities to class labels
cm = confusion_matrix(y_test, y_pred_class)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)

disp.plot()
plt.title('Confusion Matrix for QDA')


