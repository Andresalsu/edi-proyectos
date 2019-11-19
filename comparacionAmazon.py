import boto3
import os
import json
import base64

def compare_faces(sourceFile, targetFile):

    client=boto3.client('rekognition')
   
    imageSource=open(sourceFile,'rb')
    imageTarget=open(targetFile,'rb')

    response=client.compare_faces(SimilarityThreshold=80,
                                  SourceImage={'Bytes': imageSource.read()},
                                  TargetImage={'Bytes': imageTarget.read()})
    
    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])
        print('The face at ' +
               str(position['Left']) + ' ' +
               str(position['Top']) +
               ' matches with ' + similarity + '% confidence')

    imageSource.close()
    imageTarget.close()     
    return len(response['FaceMatches'])          

def main():
    source_file='/Users/andalval/Desktop/Fotos prueba 1.jpg'
    target_file='/Users/andalval/Desktop/Fotogrupalprueba.jpg'
    face_matches=compare_faces(source_file, target_file)
    print("Face matches: " + str(face_matches))


if __name__ == "__main__":
    main()