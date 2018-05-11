import os
import time
import sys
import signal
import argparse
import logging

from verifai_sdk import VerifaiService

processing_state = True


def files_to_process(path):
    """
    Provide a directory, and it will return all files.

    If you would like to skip certain files or do something else with
    it you can do that here.

    :param path: the path to show the listing for
    :type: str
    :return list of filenames
    :rtype list
    """
    for file in os.listdir(path):
        yield file


def process_file(path, processed_path, service):
    """
    This takes a path, and processes the file and dumps it at the other
    side (processed_path).

    :param path: path to the file you want to classify
    :type path: str
    :param processed_path: path to directory you want to write it to
    :type processed_path: str
    :param service: instance of the classifier
    :type service: VerifaiService
    :return: True when successful classified, False when not
    :rtype: bool
    """
    # Classify the file
    document = service.classify_image_path(path)
    filename = os.path.basename(path)
    target_path = os.path.join(processed_path, filename)

    if not document:
        # No ID > move
        os.rename(path, target_path)
        logger.info('No document found in {0}'.format(filename))
        return False

    # ID -> delete -> write cropped and masked
    os.remove(path)
    masked_image = document.mask_zones(document.zones())
    masked_image.save(target_path)
    logger.info('Found document in {0}: {1} ({2})'.format(filename, document.model, document.country))

    return True


def signal_handler(signal, frame):
    """
    Handles the Ctrl+C command.

    :param signal: signal
    :type signal: signal
    :param frame: frame
    :type frame: frame
    :return: None
    :rtype: None
    """
    global processing_state
    logger = logging.getLogger(__name__)
    logger.info('Finishing last document, will stop after that.')
    processing_state = False


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info('Initializing Verifai Folder Watcher')

    parser = argparse.ArgumentParser(
        description='Verifai Folder Watcher')
    parser.add_argument('--watch', dest='watch_path',
                        help='Path to watch for changes',
                        default='input')
    parser.add_argument('--processed', dest='processed_path',
                        help='Path where files should be stored after processing',
                        default='output')
    parser.add_argument('--api-key', dest='api_key',
                        help='API key to use with the Verifai backend',
                        required=True)
    parser.add_argument('--classifier-url', dest='classifier_url',
                        help='The full url to the classifier webservice',
                        default='http://localhost:5000/api/classify/')
    parser.add_argument('--interval', dest='interval',
                        help='number of seconds to wait between processing',
                        default=1, type=int)
    args = parser.parse_args()

    service = VerifaiService(token=args.api_key)
    service.add_clasifier_url(args.classifier_url)

    try:
        assert os.path.isdir(args.watch_path)
    except AssertionError:
        logger.critical('Watch path is not found or not a directory.')
        sys.exit(1)

    os.makedirs(args.processed_path, exist_ok=True)

    signal.signal(signal.SIGINT, signal_handler)
    logger.info('Press Ctrl+C to stop')

    while processing_state:
        files = files_to_process(args.watch_path)
        for file in files:
            file_path = os.path.join(args.watch_path, file)
            process_file(file_path, args.processed_path, service)
            if not processing_state:
                break
        time.sleep(args.interval)
