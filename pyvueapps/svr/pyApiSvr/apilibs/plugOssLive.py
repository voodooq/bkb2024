import oss2
import logging

logger = logging.getLogger('plugOssLive')

class TOssLive:
    def __init__(self , acRouter):
        self.acRouter = acRouter
        # NOTE: 从 svrConfig 中读取 ossLive 配置，不再硬编码 AK/SK
        # 初始化时用空配置，在 pyapisvr.py 启动时通过 svrConfig 注入
        self.config = {}
        self.channel = None
        self.bucket= None
    def setConfig(self, config):
        """
        通过 svrConfig['ossLive'] 注入配置
        """
        self.config = config
    def getBucket(self):
        try:
            if self.bucket== None:
                access_key_id = self.config.get('ak', '')
                access_key_secret = self.config.get('sk', '')
                endpoint = self.config.get('endpoint', '')
                bucket_name = self.config.get('bucket', '')
                if not access_key_id or not access_key_secret:
                    logger.error('OSS Live AK/SK not configured')
                    return None
                self.bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
        except Exception as er:
            logger.error('getBucket error: %s', er)
        return  self.bucket
    def getChannel(self):
        try:
            if self.channel==None :
                bucket = self.getBucket()
                if bucket!=None:
                    channel = None
                    channelName = self.config['channel']
                    chs = oss2.LiveChannelIterator(bucket, prefix=channelName)
                    for ch in chs:
                        if ch.name == channelName:
                            channel = ch
                            break
                    if channel == None :
                        description = self.config['description']
                        playlist_name = self.config['channel']+".m3u8"
                        channel = bucket.create_live_channel(
                            channelName,
                            oss2.models.LiveChannelInfo(
                                status='enabled',
                                description= description,
                                target=oss2.models.LiveChannelInfoTarget(
                                    playlist_name=playlist_name,
                                    frag_count=3,
                                    frag_duration=5)))
                        self.channel = channel
        except Exception as er:
            logger.error('getChannel error: %s', er)
        return self.channel
    def getChannelInfo(self):
        res ={}
        try:
            ch = self.getChannel()
            if ch!=None:
                res['playUrl'] = ch.play_url
                res['pushUrl'] = ch.publish_url
                bucket = self.getBucket()
                channel_name = self.config['channel']
                playlist_name = channel_name+".m3u8"
                res['signPushUrl'] = bucket.sign_rtmp_url(channel_name, playlist_name, expires=360000)
        except Exception as er:
            logger.error('getChannelInfo error: %s', er)
        return  res
    def setVideoSplit(self, splitCode, startTime , endTime):
        res ={
            'status':0
        }
        try:
            bucket = self.getBucket()
            if bucket!=None:
                channel_name = self.config['channel']
                generate_playlist = splitCode
                if splitCode[-4]!="m3u8":
                    generate_playlist = generate_playlist +".m3u8"
                    bucket.post_vod_playlist(
                        channel_name,
                        generate_playlist,
                        start_time=startTime,
                        end_time=endTime)
                    logger.info('vod playlist: %s', generate_playlist)
                    res['status'] = 1
        except Exception as er:
            logger.error('setVideoSplit error: %s', er)
        return  res
    def acRouterSplit(self, data):
        try:
            code = data.params['code']
            start = data.params['start']
            end = data.params['end']
            self.getChannel()
            data.result = self.setVideoSplit(code , start, end)
        except Exception as er:
            logger.error('acRouterSplit error: %s', er)
    def acRouterGetChannel(self,data):
        try:
            data.result = self.getChannelInfo()
        except Exception as er:
            logger.error('acRouterGetChannel error: %s', er)
