import unittest
from src.utils import Transcriber


valid_wav_path = "downloads"
unvalid_wav_path = "\/"
valid_download_folder = "downloads"
unvalid_download_folder = "\/" 
valid_video_length_in_seconds = 60
unvalid_video_length_in_seconds = -1
valid_model_name = ["tiny", "tiny.en", "base", "base.en",
                  "small", "small.en", "medium", "medium.en",
                  "large", "large-v1", "large-v2", "large-v3"]
unvalid_model_name = []
valid_language_code = "EN"
unvalid_language_code = "english"


class TestTranscriber (unittest.TestCase):
    def setUp(self,wav_path, download_folder, video_length_in_seconds, model_name, language_code):
        self.transcriber = Transcriber(wav_path, download_folder, video_length_in_seconds, model_name, language_code)
    
    def testTranscriberValidWavPath(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, valid_model_name, valid_language_code)
        # garantir que a transcrição foi feita corretamente
        
    def testTranscriberUnvalidWavPath(self):
        self.setUp(unvalid_wav_path, valid_download_folder, valid_video_length_in_seconds, valid_model_name, valid_language_code)
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
    
    def testTranscriberValidDownloadFolder(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, valid_model_name, valid_language_code)
        # garantir que a transcrição foi feita corretamente
        
    def testTranscriberUnvalidDownloadFolder(self):
        self.setUp(valid_wav_path, unvalid_download_folder, valid_video_length_in_seconds, valid_model_name, valid_language_code)
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
        
    def testTranscriberValidVideoLength(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, valid_model_name, valid_language_code)
        # garantir que a transcrição foi feita corretamente
        
    def testTranscriberUnvalidVideoLength(self):
        self.setUp(valid_wav_path, valid_download_folder, unvalid_video_length_in_seconds, valid_model_name, valid_language_code)
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
            
    def testTranscriberValidModelName(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, valid_model_name, valid_language_code)
        # garantir que a transcrição foi feita corretamente
        
    def testTranscriberUnvalidModelNameTiny(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, unvalid_model_name[0], valid_language_code)    
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
    
    def testTranscriberUnvalidModelNameTinyen(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, unvalid_model_name[1], valid_language_code)    
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
    
    def testTranscriberUnvalidModelNameBase(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, unvalid_model_name[2], valid_language_code)    
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
    
    def testTranscriberUnvalidModelNameBaseen(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, unvalid_model_name[3], valid_language_code)    
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
    
    def testTranscriberUnvalidModelNameSmall(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, unvalid_model_name[4], valid_language_code)    
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
    
    def testTranscriberUnvalidModelNameSmallbe(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, unvalid_model_name[5], valid_language_code)    
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
    
    def testTranscriberUnvalidModelNameMedium(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, unvalid_model_name[6], valid_language_code)    
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
    
    def testTranscriberUnvalidModelNameMediumbe(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, unvalid_model_name[7], valid_language_code)    
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
    
    def testTranscriberUnvalidModelNameLarge(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, unvalid_model_name[8], valid_language_code)    
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
    
    def testTranscriberUnvalidModelNameLargeV1(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, unvalid_model_name[9], valid_language_code)    
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
    
    def testTranscriberUnvalidModelNameLargeV2(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, unvalid_model_name[10], valid_language_code)    
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
    
    def testTranscriberUnvalidModelNameLargeV3(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, unvalid_model_name[11], valid_language_code)    
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
    
    def testTranscriberValidLanguageCode(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, valid_model_name, valid_language_code)
        # garantir que a transcrição foi feita corretamente
    
    def testTranscriberUnvalidLanguageCode(self):
        self.setUp(valid_wav_path, valid_download_folder, valid_video_length_in_seconds, valid_model_name, unvalid_language_code)
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,)
        
    
    
if __name__ == "__main__":
    unittest.main()