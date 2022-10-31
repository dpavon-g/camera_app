from azure.cognitiveservices.vision.face import FaceClient 
from azure.cognitiveservices.vision.face.models import DetectedFace,FaceAttributeType,VerifyResult , IdentifyResult , IdentifyCandidate , SimilarFace
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person , TrainingStatus , PersonGroup
# from config import DefaultConfig
import asyncio
import time
from io import BytesIO
import requests

class FaceCognitive():

    def __init__(self) : 
        API_KEY = "25e931d673ab47558d1a9aea13c61fc4"
        ENDPOINT = "https://facevisionid.cognitiveservices.azure.com/"

        self.face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

     
    def faceAnalysis(self , image : BytesIO , mode : str = None ) -> DetectedFace :
        #se non presente viene effettuata analisi approfondita   
        if mode != "onlyId" :
        
            self.detected_face = self.face_client.face.detect_with_stream(
                image ,
                return_face_attributes=[
                    FaceAttributeType.age,
                    FaceAttributeType.emotion,
                    FaceAttributeType.gender,
                    FaceAttributeType.makeup,
                    FaceAttributeType.facial_hair,
                    FaceAttributeType.glasses
                ],
                recognition_model="recognition_03"

            )
        #viene restiututio solo id per successive analisi
        else : 
            self.detected_face = self.face_client.face.detect_with_stream(image , recognition_model="recognition_03")
    
        if not self.detected_face : 

            return None
        else : 
            #return primo viso disponibile
            return self.detected_face[0]

    def faceCompare( self, Photo1, Photo2) -> VerifyResult :
        #compare tra due visi da cui recupero l'id per il confronto
        image1 = open(Photo1, 'rb')
        image2 = open(Photo2, 'rb')

        self.face1 : DetectedFace =  self.faceAnalysis(image1 , "onlyId")
        self.face2 : DetectedFace =  self.faceAnalysis(image2 , "onlyId")


        if (self.face1 != None ) and (self.face2 != None) : 

            result : VerifyResult = self.face_client.face.verify_face_to_face(self.face1.face_id , self.face2.face_id )

            return result
        else : 
            return None

def main():
    print(FaceCognitive().faceCompare())