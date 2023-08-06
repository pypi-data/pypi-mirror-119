import pandas as pd
import pandas as pd
import numpy as np
from spacy.lang.en import English
from tabulate import tabulate
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from pyAutoML.ml import ML,ml, EncodeCategorical
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

class prosesData:  
  def __init__(self, namaFile):
      self.dataFile = namaFile

  def fulldataset(self, inputSRS= 'SRS1'):
      xl = pd.ExcelFile(self.dataFile)
      dfs = {sh:xl.parse(sh) for sh in xl.sheet_names}
      kalimat = dfs[inputSRS]
      kalimat_semua = kalimat.head(len(kalimat))
      return kalimat_semua

  def preprocessing(self):
      xl = pd.ExcelFile(self.dataFile)
      for sh in xl.sheet_names:
        df = xl.parse(sh)
        print('Processing: [{}] ...'.format(sh))
        print(df.head())

  def apply_cleaning_function_to_list(self, X):
      cleaned_X = []
      for element in X:
          cleaned_X.append(prosesData.clean_text(self, raw_text= element))
      return cleaned_X

  def clean_text(self, raw_text):
      nlp = English()
      tokenizer = nlp.Defaults.create_tokenizer(nlp)
      tokens = tokenizer(raw_text)
      lemma_list = [token.lemma_.lower() for token in tokens if token.is_stop is False and token.is_punct is False and token.is_alpha is True]
      joined_words = ( " ".join(lemma_list))
      return joined_words  


class pengukuranEvaluasi:
  def __init__(self, dataPertama, dataKedua):
      self.data1 = dataPertama
      self.data2 = dataKedua

  def kmeans_cluster(self, nilai_cluster= 3):
      XVSM = np.array(self.data1)
      yVSM = np.array(self.data2)
      kmeans = KMeans(n_clusters=nilai_cluster) # You want cluster the passenger records into 2: Survived or Not survived
      kmeans.fit(XVSM)
      correct = 0
      for i in range(len(XVSM)):
          predict_me = np.array(XVSM[i].astype(float))
          predict_me = predict_me.reshape(-1, len(predict_me))
          prediction = kmeans.predict(predict_me)
          if prediction[0] == yVSM.all():
              correct += 1
      scaler = MinMaxScaler()
      XVSM_scaled = scaler.fit_transform(yVSM)
      print("data_correction {}".format(correct/len(XVSM)))
      return (XVSM_scaled)


  def ukur_evaluasi(self):
      X_train, X_test, y_train, y_test = train_test_split(pengukuranEvaluasi.kmeans_cluster(self), self.data2, test_size=0.3,random_state=109) # 70% training and 30% test
      y_train = y_train.argmax(axis= 1)
      X = X_train
      Y = y_train
      Y = EncodeCategorical(Y)
      size = 0.4
      return ML(X, Y, size, SVC(), RandomForestClassifier(), DecisionTreeClassifier(), KNeighborsClassifier(), LogisticRegression(max_iter = 7000))      

if __name__ == "__main__":
    myData = prosesData() # myData.preprocessing()
    req = myData.fulldataset() # myData.fulldataset(inputSRS)
    text_to_clean = list(req['Requirement Statement'])
    cleaned_text = myData.apply_cleaning_function_to_list(text_to_clean)
