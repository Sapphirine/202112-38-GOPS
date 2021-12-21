from scipy import spatial
import numpy as np 

conoray_training_correlation = np.load('coronary_training_correlation.npy')
conoray_validation_correlation = np.load('coronary_validation_correlation.npy')
print('conoray correlation(pearson) cosine:')
print(spatial.distance.cosine(conoray_training_correlation, conoray_validation_correlation))

stroke_training_correlation = np.load('stroke_training_correlation.npy')
stroke_validation_correlation = np.load('stroke_validation_correlation.npy')
print('stroke correlation(pearson) cosine:')
print(spatial.distance.cosine(stroke_training_correlation, stroke_validation_correlation))

conoray_training_correlation_kendall = np.load('coronary_training_correlation_kendall.npy')
conoray_validation_correlation_kendall = np.load('coronary_validation_correlation_kendall.npy')
print('conoray correlation(kendall) cosine:')
print(spatial.distance.cosine(conoray_training_correlation_kendall, conoray_validation_correlation_kendall))

stroke_training_correlation_kendall = np.load('stroke_training_correlation_kendall.npy')
stroke_validation_correlation_kendall = np.load('stroke_validation_correlation_kendall.npy')
print('stroke correlation(kendall) cosine:')
print(spatial.distance.cosine(stroke_training_correlation_kendall, stroke_validation_correlation_kendall))

conoray_training_correlation_spearman = np.load('coronary_training_correlation_spearman.npy')
conoray_validation_correlation_spearman = np.load('coronary_validation_correlation_spearman.npy')
print('conoray correlation(spearman) cosine:')
print(spatial.distance.cosine(conoray_training_correlation_spearman, conoray_validation_correlation_spearman))

stroke_training_correlation_spearman = np.load('stroke_training_correlation_spearman.npy')
stroke_validation_correlation_spearman = np.load('stroke_validation_correlation_spearman.npy')
print('stroke correlation(spearman) cosine:')
print(spatial.distance.cosine(stroke_training_correlation_spearman, stroke_validation_correlation_spearman))