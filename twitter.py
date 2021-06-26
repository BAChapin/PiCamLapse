from global_variables import TwitterSettings
from global_variables import GeneralSettings
from twython import Twython

class Tweet:

    def post_image(path: str, photo_number: int):
        if TwitterSettings.enabled:
            twitter = Twython(TwitterSettings.api_key,
                              TwitterSettings.api_secret,
                              TwitterSettings.access_token,
                              TwitterSettings.access_token_secret)
            message = "#PiCamLapse just took its {} day photo on {}. #TimeLapse".format(photo_number, GeneralSettings.pi_identifier)
            image = open(path, "rb")
            response = twitter.upload_media(media=image)
            media_id = [response["media_id"]]
            twitter.update_status(status=message, media_ids=media_id)

            return True
        else:
            return False
