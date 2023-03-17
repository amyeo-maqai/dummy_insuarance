from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import pandas as pd
import pickle,os
from insurancebase.settings import BASE_DIR
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
# Create your views here.

cols_to_delete_due_to_missing_data = ['Insurance_History_5',
                                      'Family_Hist_2', 'Family_Hist_3', 'Family_Hist_5',
                                      'Medical_History_10', 'Medical_History_15', 'Medical_History_24', 'Medical_History_32']

def test(request):
    return render(request,"index.html")


def load():
    mm_scaller = pickle.load(open(os.path.join(BASE_DIR,'model/MM_scaler.pkl'),'rb'))
    oh_encoder  = pickle.load(open(os.path.join(BASE_DIR,'model/OH_encoder.pkl'),'rb'))
    rf_model = pickle.load(open(os.path.join(BASE_DIR,'model/rf_model.pkl'),'rb'))
    return mm_scaller,oh_encoder,rf_model
    
mm_scaller,oh_enocder,rf_model = load()

class upl(APIView):
    parser_classes = (FormParser,MultiPartParser,FileUploadParser)

    def get(self, request):
        return Response("GET API")

    def post(self, request):
        df_new = pd.DataFrame()
        try:
            file = request.data['file']
            if str(file).endswith(".csv"):
                # print(oh_enocder)
                df = pd.read_csv(file)
                OH_col = ['Product_Info_2']
                # print(df['Product_Info_2'])
                df_trans = pd.DataFrame(oh_enocder.transform(df[OH_col]))
                df_trans.index = df.index
                # print(df_trans.columns,oh_enocd   er.get_feature_names_out(OH_col))
                df_trans.columns = oh_enocder.get_feature_names_out(OH_col)
                df.drop(OH_col,axis=1,inplace = True)
                df.drop(cols_to_delete_due_to_missing_data,axis=1,inplace = True)
                df = pd.concat([df,df_trans],axis=1)
                df = df.set_index('Id')
                # print(df.shape)
                df_new = df[mm_scaller.get_feature_names_out()]
                    # df_new = pd.concat([df_new,df[col_name]],axis=1)
                data = pd.DataFrame(mm_scaller.transform(df_new),index = df_new.index,columns = df_new.columns)
                y_pred = rf_model.predict(data)
                print(y_pred)
            content_type = file.content_type
            response = "predicted risk level of the given input data is:- level {} ".format(y_pred[0])
        except Exception as e:
            response = str(e)
        return Response({"message":response,
                         "status":200})