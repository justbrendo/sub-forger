import unittest
from ..src.main import download_video,download_thumbnail,convert_video_to_audio,burn_subtitles

valid_URL = "https://www.youtube.com/watch?app=desktop&v=biESGy2iDUQ"
unvalid_URL = "https://www.youtube.com/watch?app=desktop&v=biESGy"

unvalid_path = "\/"
valid_path = "downloads"
valid_path_video = "downloads/video.mp4"
unvalid_path_video = "downloads/video"
valid_path_subtitles = "downloads/subs.str"
unvalid_path_subtitles = "downloads/subs"

class TestDownloader (unittest.TestCase):
    def setUp(self):
        pass
        
    def testValidURLDownloadVideo(self):
        # confirmar se o download foi realmente feito
        download_video(valid_URL)
        
    def testUnvalidtURLDownloadVideo(self):
        download_video(unvalid_URL)
        # capturar a excessão com o assert 
        # self.assertRaises(Exception,download_video(unvalid_URL))
    
    def testResolution144p(self):
        self.assertEqual(download_video(valid_URL,"144p")[5],"144p")
        
    def testResolution240p(self):
        self.assertEqual(download_video(valid_URL,"240p")[5],"240p")
    
    def testResolution360p(self):
        self.assertEqual(download_video(valid_URL,"360p")[5],"360p")
        
    def testResolution720p(self):
        self.assertEqual(download_video(valid_URL,"720p")[5],"720p")
    
    def testValidURLDownloadThumbnail(self):
        # confirmar se o download foi realmente feito
        download_thumbnail(valid_URL,valid_path)
        
    def testUnvalidtURLDownloadThumbnail(self):
        download_thumbnail(unvalid_URL,valid_path)
        # capturar a excessão com o assert
        #self.assertRaises(Exception,download_thumbnail(unvalid_URL,valid_path))
    
    def testValidPath(self):
        # confirmar se o download foi realmente feito
        download_thumbnail(valid_URL,valid_path)
        
    def testUnvalidtPath(self):
        download_thumbnail(unvalid_URL,unvalid_path)
        # capturar a excessão com o assert
        # self.assertRaises(Exception,download_thumbnail(unvalid_URL,unvalid_path))
    
    def testValidtVideoPathConvertVideoToAudio(self):
        # confirmar se a conversão foi realmente feita
        convert_video_to_audio(valid_path_video,valid_path,"title")
    
    def testUnvalidtVideoPathConvertVideoToAudio(self):
        convert_video_to_audio(unvalid_path_video,valid_path,"title")
        # capturar a excessão com o assert
        # self.assertRaises(Exception,convert_video_to_audio(unvalid_path_video,valid_path,"title"))
        
    def testValidtAudioPathConvertVideoToAudio(self):
        # confirmar se a conversão foi realmente feita
        convert_video_to_audio(valid_path_video,valid_path,"title")
    
    def testUnvalidtAudioPathConvertVideoToAudio(self):
        convert_video_to_audio(valid_path_video,unvalid_path,"title")
        # capturar a excessão com o assert
        # self.assertRaises(Exception,convert_video_to_audio(valid_path_video,unvalid_path,"title"))
        
    def testValidtVideoPathBurnSubtitles(self):
        # confirmar se os subtitulos foram acrescentados
        burn_subtitles(valid_path_video,valid_path,valid_path)
    
    def testUnvalidtVideoPathBurnSubtitles(self):
        burn_subtitles(unvalid_path_video,valid_path,valid_path)
        # capturar a excessão com o assert
        # self.assertRaises(Exception,burn_subtitles(unvalid_path_video,valid_path,valid_path))
        
    def testValidtSubtitlePathBurnSubtitles(self):
        # confirmar se os subtitulos foram acrescentados
        burn_subtitles(valid_path_video,valid_path_subtitles,valid_path)
    
    def testUnvalidtSubtitlePathBurnSubtitles(self):
        burn_subtitles(valid_path_video,unvalid_path_subtitles,valid_path)
        # capturar a excessão com o assert
        # self.assertRaises(Exception,burn_subtitles(valid_path_video,unvalid_path_subtitles,valid_path))
    
    def testValidtOutPutPathBurnSubtitles(self):
        # confirmar se os subtitulos foram acrescentados
        burn_subtitles(valid_path_video,valid_path_subtitles,valid_path)
    
    def testUnvalidtOutPutPathBurnSubtitles(self):
        burn_subtitles(valid_path_video,valid_path_subtitles,unvalid_path)
        # capturar a excessão com o assert
        # self.assertRaises(Exception,burn_subtitles(valid_path_video,valid_path_subtitles,unvalid_path))
    

if __name__ == "__main__":
        unittest.main()


        