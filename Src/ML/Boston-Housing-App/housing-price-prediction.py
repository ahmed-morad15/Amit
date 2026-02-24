
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, root_mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score


df = pd.read_csv("C:/DEPI/Amit/Src/ML/Boston-Housing-App/BostonHousing.csv")
df.head()

# take a look at the summary of the dataset
df.info()

# ckeck for null values
df.isna().sum()

# check for any negative values in the medv column (no negative values)
df[df['medv'] < 0]

# Statistical summary for all numerical columns
df.describe()

# ckeck for the correlation between the columns using heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.show()

# deal with missing values
df["rm"].fillna(df["rm"].mean(), inplace=True)
df.isna().sum()


num_cols = df.select_dtypes(include=['int64', 'float64']).columns
plt.figure(figsize=(20, 2))
for i, col in enumerate(num_cols):
    plt.subplot(1, len(num_cols), i + 1)
    sns.boxplot(df[col],orient='h')
    plt.title(f'Boxplot of {col}')

# Handling outliers using IQR method
def handle_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df[column] = np.where(df[column] < lower_bound, lower_bound, df[column])
    df[column] = np.where(df[column] > upper_bound, upper_bound, df[column])
    return df

numerical_cols = df.select_dtypes(include='number').columns
for col in numerical_cols:
    df = handle_outliers(df, col)


num_cols = df.select_dtypes(include=['int64', 'float64']).columns
plt.figure(figsize=(20, 2))
for i, col in enumerate(num_cols):
    plt.subplot(1, len(num_cols), i + 1)
    sns.boxplot(df[col],orient='h')
    plt.title(f'Boxplot of {col}')


# Splitting features and target
X = df.drop('medv', axis=1)
y = df['medv']


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features (to ensure that all features contribute equally to the model)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


def plot_predictions(y_test, predictions, model_name):
    import matplotlib.pyplot as plt
    import numpy as np

    y_test = np.array(y_test)
    predictions = np.array(predictions)

    plt.figure(figsize=(8, 6))

    # Scatter plot of actual vs predicted values
    plt.scatter(y_test, predictions, color='skyblue', edgecolor='k', alpha=0.7, label='Predicted vs Actual')

    # Diagonal line for perfect predictions
    min_val = np.min(y_test)
    max_val = np.max(y_test)
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')

    # Adding labels and title
    plt.xlabel('Actual Values', fontsize=12)
    plt.ylabel('Predicted Values', fontsize=12)
    plt.title(f'{model_name} Predictions vs Actual Values', fontsize=14)

    # Adding legend and grid
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()


# Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_predictions = lr_model.predict(X_test)

# Evaluation
print("Linear Regression R2 Score:", r2_score(y_test, lr_predictions))
print("Linear Regression MSE:", mean_squared_error(y_test, lr_predictions))
print("Linear Regression RMSE:", root_mean_squared_error(y_test, lr_predictions))

# Plot for Linear Regression
lr_predictions_array = np.array(lr_predictions)
plot_predictions(y_test, lr_predictions_array, 'Linear Regression')

# Decision Tree Regressor
dt_model = DecisionTreeRegressor(random_state=42)
dt_model.fit(X_train, y_train)
dt_predictions = dt_model.predict(X_test)

# Evaluation
print("Decision Tree R2 Score:", r2_score(y_test, dt_predictions))
print("Decision Tree MSE:", mean_squared_error(y_test, dt_predictions))
print("Decision Tree RMSE:", root_mean_squared_error(y_test, dt_predictions))

# Plot for Decision Tree Regressor
dt_predictions_array = np.array(dt_predictions)
plot_predictions(y_test, dt_predictions_array, 'Decision Tree Regressor')

# Random Forest Regressor
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)

# Evaluation
print("Random Forest R2 Score:", r2_score(y_test, rf_predictions))
print("Random Forest MSE:",mean_squared_error(y_test, rf_predictions))
print("Random Forest RMSE:",root_mean_squared_error(y_test, rf_predictions))

# Plot for Random Forest Regressor
rf_predictions_array = np.array(rf_predictions)
plot_predictions(y_test, rf_predictions_array, 'Random Forest Regressor')


lr_predictions = lr_model.predict(X_test)
dt_predictions = dt_model.predict(X_test)
rf_predictions = rf_model.predict(X_test)

lr_mse = mean_squared_error(y_test, lr_predictions)
lr_rmse = np.sqrt(lr_mse)
lr_r2 = r2_score(y_test, lr_predictions)

dt_mse = mean_squared_error(y_test, dt_predictions)
dt_rmse = np.sqrt(dt_mse)
dt_r2 = r2_score(y_test, dt_predictions)

rf_mse = mean_squared_error(y_test, rf_predictions)
rf_rmse = np.sqrt(rf_mse)
rf_r2 = r2_score(y_test, rf_predictions)

models = ['Linear Regression', 'Decision Tree', 'Random Forest']
mse_scores = [lr_mse, dt_mse, rf_mse]
rmse_scores = [lr_rmse, dt_rmse, rf_rmse]
r2_scores = [lr_r2, dt_r2, rf_r2]


bar_width = 0.25
index = np.arange(len(models))
fig, ax = plt.subplots(figsize=(12, 8))

bar1 = ax.bar(index - bar_width, mse_scores, bar_width, label='MSE', color='#3498db', edgecolor='darkblue')
bar2 = ax.bar(index, rmse_scores, bar_width, label='RMSE', color='#e67e22', edgecolor='darkorange')
bar3 = ax.bar(index + bar_width, r2_scores, bar_width, label='R²', color='#2ecc71', edgecolor='darkgreen')

ax.set_xlabel('Models', fontsize=14)
ax.set_ylabel('Scores', fontsize=14)
ax.set_title(' Model Performance on Test Set ', fontsize=16, fontweight='bold')
ax.set_xticks(index)
ax.set_xticklabels(models, fontsize=12)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3, axis='y')

for bars in [bar1, bar2, bar3]:
    for bar in bars:
        yval = bar.get_height()
        if bars == bar3:  
            ax.text(bar.get_x() + bar.get_width()/2, yval + 0.02, 
                   f'{yval:.3f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        else:  
            ax.text(bar.get_x() + bar.get_width()/2, yval + max(mse_scores)*0.02, 
                   f'{yval:.2f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()


test_results_df = pd.DataFrame({
    'Model': ['Linear Regression', 'Decision Tree', 'Random Forest'],
    'R2': [lr_r2, dt_r2, rf_r2],
    'MSE': [lr_mse, dt_mse, rf_mse],
    'RMSE': [lr_rmse, dt_rmse, rf_rmse]
})

test_results_df = test_results_df[['Model', 'R2', 'MSE', 'RMSE']]
test_results_df.style.format({'R2': "{:.4f}",
                              'MSE': "{:.2f}",
                              'RMSE': "{:.2f}"
                              }).set_caption(" Test Set Results for Regression Models")



def cross_validate_model(model, X, y, cv=5):
    mse_scores = -cross_val_score(model, X, y, cv=cv, scoring='neg_mean_squared_error')
    rmse_scores = np.sqrt(mse_scores)
    r2_scores = cross_val_score(model, X, y, cv=cv, scoring='r2')
    return np.mean(mse_scores), np.mean(rmse_scores), np.mean(r2_scores)

#  Cross-validation for each model
lr_cv_mse, lr_cv_rmse, lr_cv_r2 = cross_validate_model(lr_model, X_train, y_train)
dt_cv_mse, dt_cv_rmse, dt_cv_r2 = cross_validate_model(dt_model, X_train, y_train)
rf_cv_mse, rf_cv_rmse, rf_cv_r2 = cross_validate_model(rf_model, X_train, y_train)


# Cross-validation results
models = ['Linear Regression', 'Decision Tree', 'Random Forest']
mse_scores = [lr_cv_mse, dt_cv_mse, rf_cv_mse]
rmse_scores = [lr_cv_rmse, dt_cv_rmse, rf_cv_rmse]
r2_scores = [lr_cv_r2, dt_cv_r2, rf_cv_r2]

bar_width = 0.25
index = np.arange(len(models))
fig, ax = plt.subplots(figsize=(12, 8))

bar1 = ax.bar(index - bar_width, mse_scores, bar_width, label='MSE', color='#3498db', edgecolor='darkblue')
bar2 = ax.bar(index, rmse_scores, bar_width, label='RMSE', color='#e67e22', edgecolor='darkorange')
bar3 = ax.bar(index + bar_width, r2_scores, bar_width, label='R²', color='#2ecc71', edgecolor='darkgreen')

ax.set_xlabel('Models', fontsize=14)
ax.set_ylabel('Scores', fontsize=14)
ax.set_title(' Model Performance on Test Set ', fontsize=16, fontweight='bold')
ax.set_xticks(index)
ax.set_xticklabels(models, fontsize=12)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3, axis='y')

for bars in [bar1, bar2, bar3]:
    for bar in bars:
        yval = bar.get_height()
        if bars == bar3:  
            ax.text(bar.get_x() + bar.get_width()/2, yval + 0.02, 
                   f'{yval:.3f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        else:  
            ax.text(bar.get_x() + bar.get_width()/2, yval + max(mse_scores)*0.02, 
                   f'{yval:.2f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()


cv_results_df = pd.DataFrame({
    'Model': ['Linear Regression', 'Decision Tree', 'Random Forest'],
    'R2': [lr_cv_r2, dt_cv_r2, rf_cv_r2],
    'MSE': [lr_cv_mse, dt_cv_mse, rf_cv_mse],
    'RMSE': [lr_cv_rmse, dt_cv_rmse, rf_cv_rmse]
})

cv_results_df = test_results_df[['Model', 'R2', 'MSE', 'RMSE']]
cv_results_df.style.format({'R2': "{:.4f}",
                              'MSE': "{:.2f}",
                              'RMSE': "{:.2f}"
                              }).set_caption(" Cross-Validation Results for Regression Models")


best_model_idx = (test_results_df['R2'] - 
                  test_results_df['RMSE']/test_results_df['RMSE'].max()).idxmax()

best_model_df = test_results_df.loc[[best_model_idx]].copy()

best_model_df.style \
    .format({'R2': "{:.4f}", 'MSE': "{:.2f}", 'RMSE': "{:.2f}"}) \
    .set_caption(" Best Model") \
    .background_gradient(cmap='YlGnBu', subset=['R2']) \
    .background_gradient(cmap='OrRd_r', subset=['RMSE'])


import pickle
# Save the best model as a .pkl file
model_path = 'C:/DEPI/Amit/Src/ML/Boston-Housing-App/Boston_Housing_Best_model.pkl'
with open(model_path, 'wb') as model_file:
    pickle.dump(rf_model, model_file)

print(f" model saved as '{model_path}'")

# Save the scaler as a .pkl file
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)