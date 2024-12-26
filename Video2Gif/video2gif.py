#
# Orbital Intelligence Python Coding Samples 
#
# Video2Gif - Generate a .gif file from a video file
#
# Copyright 2024 Orbital Intelligence LLC
#
# Standard Python libraries (>=3.11)
#
# Run: pip install -r requirements.txt
#
# Reference: https://zulko.github.io/moviepy/index.html
#

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import os
import argparse
from argparse import RawTextHelpFormatter
from datetime import (datetime, timedelta, date, timezone)
import logging
import traceback 
from moviepy import VideoFileClip

# Program Version 
VERSION = '2024.12.26'
COPYRIGHT = '2024'

# Global Directory settings
utc = datetime.now(timezone.utc)
directoryDate = utc.strftime('%Y.%m.%d_%H.%M') 
filenameDateTime = utc.strftime('%Y.%m.%d_%H.%M.%S') 
baseDirectory = os.path.join(os.getcwd(), 'Video2Gif_Artifacts', directoryDate)
logsDirectory = baseDirectory

# Globals
LOG_FILENAME = os.path.join(logsDirectory, f'Video2GifLog_{filenameDateTime}z.log')
log = logging.getLogger(__name__)


def ConfigureLogging():
    logging.basicConfig(format='%(asctime)s - %(message)s', 
                        level=logging.WARNING, 
                        encoding='utf-8',
                        datefmt='%Y-%m-%d %H:%M:%S', 
                        handlers=[logging.FileHandler(filename=LOG_FILENAME, encoding='utf-8', mode='w'),
                                  logging.StreamHandler()
                                 ]
                       )

def GenerateGifFile(sourceFile, destFile):
    try:
        videoFileClip = VideoFileClip(sourceFile)
        videoFileClip.write_gif(destFile)
    except Exception as ex:
        log.error(f'Error processing {sourceFile}: {ex}')

def GetCommandLine():
    counter = 0
    strCmdLine = 'python'

    # Build command line string
    for x in sys.argv:
        log.debug(f'{counter}: {x}')
        strCmdLine = f'{strCmdLine} {x}'
        log.debug(f'{counter}: {strCmdLine}')
        counter+=1

    return strCmdLine


def main():
    #
    # Setup logging
    #

    # Confirm local logging directory exists, create it if necessary
    logPath = os.path.dirname(LOG_FILENAME)
    if not os.path.exists(logPath):
        os.makedirs(logPath)
    # Configure logger settings
    ConfigureLogging()

    #
    # Proceed with the program
    #

    log.critical('     ____       __    _ __        __   ____      __       __')
    log.critical('    / __ \\_____/ /_  (_) /_____ _/ /  /  _/___  / /____  / /')
    log.critical('   / / / / ___/ __ \\/ / __/ __ `/ /   / // __ \\/ __/ _ \\/ / ')
    log.critical('  / /_/ / /  / /_/ / / /_/ /_/ / /  _/ // / / / /_/  __/ /  ')
    log.critical('  \\____/_/  /_.___/_/\\__/\\__,_/_/  /___/_/ /_/\\__/\\___/_/   ')
    log.critical('')
    log.critical('##############################################################')
    log.critical('01001111 01110010 01100010 01101001 01110100 01100001 01101100')
    log.critical('00100000 01001001 01101110 01110100 01100101 01101100 00000000')
    log.critical('==============================================================')
    log.critical('')
    log.critical('                            Orbital Intel                     ')
    log.critical('                    Video file to .GIF Converter              ')
    log.critical('')
    log.critical('==============================================================')
    log.critical('01001111 01110010 01100010 01101001 01110100 01100001 01101100')
    log.critical('00100000 01001001 01101110 01110100 01100101 01101100 00000000')
    log.critical('##############################################################')
    log.critical('')
    log.critical(f'Copyright (c) {COPYRIGHT} Orbital Intelligence LLC')
    log.critical(f'Version {VERSION}')
    log.critical('')

    # Configure and Process command line arguments
    parser = argparse.ArgumentParser(description='Video2Gif - video file to .GIF Conversion Utility'
		, prog='Video2Gif.py'
		, formatter_class=RawTextHelpFormatter)

    parser.add_argument('sourcefile', help=f'Provide the source video file that will be converted to a .gif file.')
    parser.add_argument('--destfile',  '-df', default='', help='Custom .gif filename.\nDefault destfile is sourcefile.gif.')
    parser.add_argument('--verbose',  '-v', action='store_true', help='Flag to display verbose output \nVerbose output is disabled by default')
    args = parser.parse_args()

    # Apply the verbose output setting
    if args.verbose:
        log.level=logging.DEBUG

    # Collect the source data to hash
    sourceFile = args.sourcefile

    # Set the destination filename
    destFile = args.destfile
    if (len(destFile) < 5) or (destFile.find('.gif') == -1):
        fileName, fileExtension = os.path.splitext(os.path.basename(sourceFile))
        destFile = f'{fileName}.gif'
        
    try:
        # Get the current datetime
        startUtcDatetime = datetime.now(timezone.utc)
        startLocalDatetime = datetime.now()

        # Display program configuration data
        log.critical('')
        log.critical(f'Command line:     {GetCommandLine()}')
        log.critical(f'Source PNG File:  {sourceFile}')
        log.critical(f'Output GIF File:  {destFile}')
        log.critical('')

        # Process the video file to .gif file conversion
        log.critical(f'Converting {os.path.basename(sourceFile)} to a .GIF file...')
        GenerateGifFile(sourceFile, destFile)
        log.critical(f'Generated {destFile}')

    except KeyboardInterrupt:
        log.critical('')
        log.critical('#############################################')
        log.critical('Video2Gif.py aborted by user.')
        log.critical('#############################################')
        sys.exit(0)
    except Exception as error:
        log.critical('#############################################')
        log.critical('General Error during Video2Gif.py processing.')
        log.critical('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        log.critical(f'Error: {error}')
        log.critical(f'Call Stack:\n{traceback.format_exc()}')
        log.critical('#############################################')
    finally: 
        # Execution completed 
        endUtcDatetime = datetime.now(timezone.utc)
        endLocalDatetime = datetime.now()

        executionTime = endLocalDatetime-startLocalDatetime
        log.critical('')
        log.debug(f'Video2Gif processing started at:   {startLocalDatetime}L / {startUtcDatetime}Z')
        log.debug(f'Video2Gif processing completed at: {endLocalDatetime}L / {endUtcDatetime}Z')
        log.debug('')
        log.critical(f'Video2Gif processing time:   {executionTime} ')
        log.critical('')
        log.critical(f'.gif file: {os.path.join(baseDirectory, destFile)}')
        log.critical('')
        log.critical(f'Log file:  {LOG_FILENAME}')
        log.critical('')
        log.critical('######################################################')
        log.critical('Video2Gif completed.   ')
        log.critical('######################################################')


if __name__ == '__main__':
    main()

