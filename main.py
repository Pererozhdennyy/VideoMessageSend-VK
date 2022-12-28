import requests


class Video:
    def __init__(self, token: str, file: str, shape_id: int = 1):
        """
        :param str token: токен юзера
        :param str file: путь к файлу
        :param int shape_id: id формы видео сообщения (1-5)
        """
        self.token = token
        self.file = file
        self.shape_id = shape_id
        self.version = '5.201'

        if self.shape_id < 1 or self.shape_id > 5:
            raise ValueError('Неверный диапазон shape_id')

    def VideoMessageUploadInfo(self) -> dict:
        params = {
            'access_token': self.token,
            'v': self.version,
            'shape_id': self.shape_id
        }
        response = requests.get('https://api.vk.com/method/video.getVideoMessageUploadInfo', params=params)
        return response.json()

    def VideoMessageUpload(self) -> dict:
        upload_url = self.VideoMessageUploadInfo()['response']['upload_url']
        response = requests.post(upload_url, files={'video_file': open(self.file, 'rb')})
        return response.json()

    def VideoMessageSend(self, peer_id: int) -> dict:
        """
        :param int peer_id: id пользователя или беседы
        """
        video_info = self.VideoMessageUpload()
        params = {
            'random_id': 0,
            'access_token': self.token,
            'v': self.version,
            'peer_id': peer_id,
            'attachment': f"video_message{video_info['owner_id']}_{video_info['video_id']}"
        }
        response = requests.get('https://api.vk.com/method/messages.send', params=params)
        return response.json()


access_token = 'token'  # vk.com, app_id - 6287487 (для метода video.getVideoMessageUploadInfo)
video = Video(access_token, 'test.mp4')
print(video.VideoMessageSend(1))
