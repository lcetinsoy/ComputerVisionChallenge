import scipy.io
import pandas as pd
from datetime import date
import datetime
import re
import numpy as np


def ordinalToDate(ordinal):
    return date.fromordinal(ordinal) + datetime.timedelta(days=ordinal % 1) - datetime.timedelta(days=366)


def removeNonAlphaNumericalCharacters(strToClean):
    return re.sub("\"|u|\[|\'|\]", lambda s: "", str(strToClean))


def binarize(age):
    return int((age > 30))

mat = scipy.io.loadmat('input/wiki_meta_data.mat')

dateOfBirths = mat['wiki']['dob'][0][0][0]
dateOfPhotoShoot = mat['wiki']['photo_taken'][0][0][0]
filePath = mat['wiki']['full_path'][0][0][0]
celebrityName = mat['wiki']['name'][0][0][0]
faceScore = mat['wiki']['face_score'][0][0][0]

wikiData = pd.DataFrame(data={

    'date_of_birth': dateOfBirths,
    'date_of_photo_shoot': dateOfPhotoShoot,

    'file_path': filePath,

})

wikiData['file_path'] = wikiData['file_path'].apply(removeNonAlphaNumericalCharacters)

wikiData['date_of_birth'] = wikiData['date_of_birth'].apply(lambda d: ordinalToDate(d))
wikiData['age'] = wikiData['date_of_photo_shoot'] - wikiData['date_of_birth'].apply(lambda d: d.year)

wikiData.replace([np.inf, -np.inf], np.nan)
wikiData.replace(np.inf, np.nan)

wikiData = wikiData.drop('date_of_birth', 1)
wikiData = wikiData.drop('date_of_photo_shoot', 1)
wikiData['label'] = wikiData['age'].apply(binarize)
cleanData = wikiData.replace([np.inf, -np.inf], np.nan).dropna()

cleanData.to_csv('output/cleaned.csv')
# wikiData.to_csv('output/example.csv')
