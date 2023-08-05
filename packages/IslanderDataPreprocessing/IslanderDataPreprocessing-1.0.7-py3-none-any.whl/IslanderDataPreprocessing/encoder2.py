import pandas as pd
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder
class Encoder:
    def __init__(self,df,type = ""):
        self.df = df.copy()
        self.type = type
    def Check(self):
        self.object_column = []
        for i in self.df.columns:
            if (self.df[i].dtype == "object"):
                self.object_column.append(i)

        if (self.object_column==[]):
            pass
        else:
            self.Correct()
        return self.df
    def Correct(self):
        if (self.type == "" or self.type.upper() == "ONEHOTENCODER"):
            self.OneHotEncoder()
        elif (self.type.upper() == "ORDINALENCODER"):
            self.OrdinalEncoder()
    def OrdinalEncoder(self):
        for i in self.object_column:
            translate = OrdinalEncoder()
            final = translate.fit_transform(self.df[i].array.reshape(-1, 1))
            self.df.drop(columns=i, inplace=True)
            self.df[i] = final

    def OneHotEncoder(self):
        for i in self.object_column:
            encoder = OneHotEncoder()
            finalencoder = encoder.fit_transform(self.df[i].array.reshape(-1, 1)).toarray()
            finalencoder = pd.DataFrame(finalencoder, columns=encoder.categories_)
            for j in finalencoder.columns:
                self.df[j] = finalencoder[j]
            self.df.drop(columns=i, inplace=True)