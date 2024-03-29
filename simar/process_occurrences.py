import os
import json
import tweepy
import logging


logger = logging.getLogger()
logging.basicConfig(filename='simar_roturas.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

#twitter loggin and api creation
def create_api():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    #logger.info("API created")
    return api


# create report message and tweet it
def send_report(tipo, elem):
    report = ""
    freguesia = ""
    local = ""
    if elem['freguesia']:
        freguesia = " na freguesia de %s" % elem['freguesia']

    if elem['local']:
        local = " no local %s" % elem['local']

    interruption_info = "%s%s com data de fim para dia %s às %s" % (freguesia, local, elem['dia'], elem['hora'])
    interruption_info = interruption_info.replace("  ", " ")
    report = "[%s]%s. #SIMAR_ROTURA" % (tipo.upper(), interruption_info.capitalize())

    logging.info(report)
    api = create_api()
    api.update_status(report)
    logging.debug("Tweet Sent")


def search_element_in_array(local, freguesia, array):
    for elem in array:
        if elem['freguesia'] == freguesia and elem['local'] == local:
            return elem
    return


def main():
    # check if there is already a processed version of occurrences
    # case not, copy current occurrences to processed
    logging.info("Running 'process_occurrences.py")

     # no file roturas - Ite means the scrapy script had problems running. Do nothing
    if not os.path.isfile('roturas.json'):
        logging.debug("No 'roturas.json' file found. Exiting")
        return
    # There is a current file to be processed
    else:

        # If there is no previous "roturas_processadas.json" file
        if not os.path.isfile('roturas_processadas.json'):
            logging.debug("No 'roturas_processadas.json' file found.")
            with open('roturas.json', 'r') as json_file:
                data = json.load(json_file)
                data = data[0]
                logging.debug("'roturas.json' file found. Processing any entry as 'NEW'.")
                # Throws Alert for each entry and in the end saves as processed file (rename file)
                for elem in data['roturas']:
                    if elem:
                        send_report("nova", elem)

                json_file.close()
                os.rename('roturas.json', 'roturas_processadas.json')
                return
        # There is a previous "roturas_processadas.json" file
        else:
            logging.debug("'roturas_processadas.json' file found. Processing entries...")
            processadas_file = open('roturas_processadas.json', 'r')
            roturas_file = open('roturas.json', 'r')
            processadas_data = json.load(processadas_file)
            processadas_data = processadas_data[0]
            roturas_data = json.load(roturas_file)
            roturas_data = roturas_data[0]


            for elem in roturas_data['roturas']:
                result = search_element_in_array(elem['local'], elem['freguesia'], processadas_data['roturas'])
                #if found a match in already processed
                if result:
                    # if although its same location has an updated resolution time
                    if not (elem['dia'] == result['dia'] and elem['hora'] == result['hora']):
                        send_report("actualizada", elem)
                # otherwise its new
                else:
                    #new occurrence
                    send_report("nova", elem)


            for processed in processadas_data['roturas']:
                result = search_element_in_array(processed['local'], processed['freguesia'], roturas_data['roturas'])
                # if not found in recent events then it was solved
                if not result:
                    send_report("resolvida", processed)

            # Close fds and rename/remove files
            processadas_file.close()
            roturas_file.close()
            os.remove('roturas_processadas.json')
            os.rename('roturas.json', 'roturas_processadas.json')
            

if __name__ == "__main__":
    main()