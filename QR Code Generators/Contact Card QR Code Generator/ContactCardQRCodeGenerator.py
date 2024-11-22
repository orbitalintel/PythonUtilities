#
# Orbital Intelligence Python Coding Samples 
#
# ContactCardQRCodeGenerator - Creates a QR Code for a VCard Contact Card that 
#                              will create a new contact when scanned with your phone
#
# Copyright 2023-2024 Orbital Intelligence LLC
#
# Standard Python libraries (>=3.11)
#
# Run: pip install -r requirements.txt
#

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import os
import argparse
from argparse import RawTextHelpFormatter
from datetime import (datetime, timedelta, date, timezone)
import logging
import traceback 
import json

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import SquareModuleDrawer, RoundedModuleDrawer, GappedSquareModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer, CircleModuleDrawer
from  qrcode.image.styles.colormasks import SolidFillColorMask

import PIL
from PIL import Image, ImageDraw

# Program Version 
VERSION = '2024.11.21'
COPYRIGHT = '2023-2024'

# Global Directory settings
utc = datetime.now(timezone.utc)
directoryDate = utc.strftime("%Y.%m.%d_%H.%M") 
filenameDateTime = utc.strftime("%Y.%m.%d_%H.%M.%S") 
baseDirectory = os.path.join(os.getcwd(), 'QRCode_Artifacts', directoryDate)
logsDirectory = baseDirectory

# Globals
LOG_FILENAME = os.path.join(logsDirectory, f'QRCodeLog_{filenameDateTime}z.log')
log = logging.getLogger(__name__)


# Constants
MODULE_DRAWER_STYLE_SQUARE = 'SquareModuleDrawer'
MODULE_DRAWER_STYLE_GAPPED_SQUARE = 'GappedSquareModuleDrawer'
MODULE_DRAWER_STYLE_VERTICAL_BARS  = 'VerticalBarsDrawer'
MODULE_DRAWER_STYLE_HORIZONTAL_BARS = 'HorizontalBarsDrawer'
MODULE_DRAWER_STYLE_ROUNDED = 'RoundedModuleDrawer'
DEFAULT_QRCODE_FILENAME = 'vcard_qr.png'
EMPTY_STRING = ''
BASE_SPACE = '   '  # Used to insert 3 'spaces' into a string


class Config:
    frontColorRed = 0
    frontColorGreen = 0
    frontColorBlue = 0
    backColorRed = 0
    backColorGreen = 0
    backColorBlue = 0

    moduleStyle = ''
    versionSize = 5

    firstName = ''
    lastName = ''
    title = ''
    organization = ''
    phone = ''
    email = ''
    url = ''
    note = ''

    destFileTimestamp = ''
    destFile = ''

    def __init__(self, configurationFile, destinationFile):
        configFile = open(configurationFile)
        configData = json.load(configFile)
        configFile.close()

        self.frontColorRed = configData['config']['FrontColor']['r']
        self.frontColorGreen = configData['config']['FrontColor']['g']
        self.frontColorBlue = configData['config']['FrontColor']['b']
        self.backColorRed = configData['config']['BackColor']['r']
        self.backColorGreen = configData['config']['BackColor']['g']
        self.backColorBlue = configData['config']['BackColor']['b']

        self.versionSize = configData['config']['Size']

        if (configData['config']['ModuleStyle'].lower() == 'gappedsquare'):
            self.moduleStyle = MODULE_DRAWER_STYLE_GAPPED_SQUARE
        elif (configData['config']['ModuleStyle'].lower() == 'verticalbars'):
            self.moduleStyle = MODULE_DRAWER_STYLE_VERTICAL_BARS
        elif (configData['config']['ModuleStyle'].lower() == 'horizontalbars'):
            self.moduleStyle = MODULE_DRAWER_STYLE_HORIZONTAL_BARS
        elif (configData['config']['ModuleStyle'].lower() == 'rounded'):
            self.moduleStyle = MODULE_DRAWER_STYLE_ROUNDED
        elif (configData['config']['ModuleStyle'].lower() == 'square'):
            self.moduleStyle = MODULE_DRAWER_STYLE_SQUARE
        else:
            self.moduleStyle = MODULE_DRAWER_STYLE_SQUARE # This is the basic/standard QR code format

        self.firstName = configData['config']['FirstName']
        self.lastName = configData['config']['LastName']
        self.title = configData['config']['Title']
        self.organization = configData['config']['Organization']
        self.phone = configData['config']['Phone']
        self.email = configData['config']['Email']
        self.url = configData['config']['Url']
        try:
            self.note = configData['config']['Note']
        except:
            self.note = ''

        try:
            self.destFileTimestamp = f'{destinationFile.split(".")[0]}_{filenameDateTime}.{destinationFile.split(".")[1]}'
            self.destFile = destinationFile
        except:
            log.error(f"Invalid destination filename [{destinationFile}]. Using the default [{DEFAULT_QRCODE_FILENAME}] filename.")
            self.destFileTimestamp = f'{DEFAULT_QRCODE_FILENAME.split(".")[0]}_{filenameDateTime}.{DEFAULT_QRCODE_FILENAME.split(".")[1]}'
            self.destFile = DEFAULT_QRCODE_FILENAME

def ConfigureLogging():
    logging.basicConfig(format='%(asctime)s - %(message)s', 
                        level=logging.WARNING, 
                        encoding='utf-8',
                        datefmt='%Y-%m-%d %H:%M:%S', 
                        handlers=[logging.FileHandler(filename=LOG_FILENAME, encoding='utf-8', mode='w'),
                                  logging.StreamHandler()
                                 ]
                       )

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

def GenerateContactCard(config):
    # contact card
    # https://en.wikipedia.org/wiki/VCard

    # Create a QR Code object
    qrContact = qrcode.QRCode(version=config.versionSize,
                              error_correction=qrcode.constants.ERROR_CORRECT_M)

    # Prepare QR Code data
    cardData = 'BEGIN:VCARD\n'\
    'VERSION:4.0\n'\
    f'N:{config.lastName};{config.firstName};;;\n'\
    f'FN:{config.firstName} {config.lastName}\n'\
    f'TITLE:{config.title}\n'\
    f'ORG:{config.organization}\n'\
    f'TEL;TYPE=work:{config.phone}\n'\
    f'EMAIL;TYPE=work:{config.email}\n'\
    f'URL:{config.url}\n'\
    f'NOTE:{config.note}\n'\
    'END:VCARD'

    log.critical(f'Card Data:\n{cardData}')
    qrContact.add_data(cardData)

    # Generate QR Code 

    # Vertical Bars 
    if (config.moduleStyle == MODULE_DRAWER_STYLE_VERTICAL_BARS):
        qr_img = qrContact.make_image(image_factory=StyledPilImage,
                                      module_drawer=VerticalBarsDrawer(),
                                      color_mask=SolidFillColorMask(
                                      back_color=(
                                        config.backColorRed, 
                                        config.backColorGreen, 
                                        config.backColorBlue), 
                                      front_color=(
                                        config.frontColorRed, 
                                        config.frontColorGreen, 
                                        config.frontColorBlue), 
                                      )
                                     )
        
    # Horizontal Bars
    elif (config.moduleStyle == MODULE_DRAWER_STYLE_HORIZONTAL_BARS):
        qr_img = qrContact.make_image(image_factory=StyledPilImage,
                                      module_drawer=HorizontalBarsDrawer(),
                                      color_mask=SolidFillColorMask(
                                      back_color=(
                                        config.backColorRed, 
                                        config.backColorGreen, 
                                        config.backColorBlue), 
                                      front_color=(
                                        config.frontColorRed, 
                                        config.frontColorGreen, 
                                        config.frontColorBlue), 
                                      )
                                     )
    
    # Gapped Squares
    elif (config.moduleStyle == MODULE_DRAWER_STYLE_GAPPED_SQUARE):
        qr_img = qrContact.make_image(image_factory=StyledPilImage,
                                      module_drawer=GappedSquareModuleDrawer(),
                                      color_mask=SolidFillColorMask(
                                      back_color=(
                                        config.backColorRed, 
                                        config.backColorGreen, 
                                        config.backColorBlue), 
                                      front_color=(
                                        config.frontColorRed, 
                                        config.frontColorGreen, 
                                        config.frontColorBlue), 
                                      )
                                     )

    # Squares - eg, the basic/standard QR code style
    elif (config.moduleStyle == MODULE_DRAWER_STYLE_SQUARE):
        qr_img = qrContact.make_image(image_factory=StyledPilImage,
                                      module_drawer=SquareModuleDrawer(),
                                      color_mask=SolidFillColorMask(
                                      back_color=(
                                        config.backColorRed, 
                                        config.backColorGreen, 
                                        config.backColorBlue), 
                                      front_color=(
                                        config.frontColorRed, 
                                        config.frontColorGreen, 
                                        config.frontColorBlue), 
                                      )
                                     )

    # Rounded - a slight variation of the basic/standard QR code style
    elif (config.moduleStyle == MODULE_DRAWER_STYLE_ROUNDED):
        qr_img = qrContact.make_image(image_factory=StyledPilImage,
                                      module_drawer=RoundedModuleDrawer(),
                                      color_mask=SolidFillColorMask(
                                      back_color=(
                                        config.backColorRed, 
                                        config.backColorGreen, 
                                        config.backColorBlue), 
                                      front_color=(
                                        config.frontColorRed, 
                                        config.frontColorGreen, 
                                        config.frontColorBlue), 
                                      )
                                     )

    # Save QR Code files
    qr_img.save(os.path.join(baseDirectory, config.destFile))
    qr_img.save(os.path.join(baseDirectory, config.destFileTimestamp))

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

    log.critical("     ____       __    _ __        __   ____      __       __")
    log.critical("    / __ \\_____/ /_  (_) /_____ _/ /  /  _/___  / /____  / /")
    log.critical("   / / / / ___/ __ \\/ / __/ __ `/ /   / // __ \\/ __/ _ \\/ / ")
    log.critical("  / /_/ / /  / /_/ / / /_/ /_/ / /  _/ // / / / /_/  __/ /  ")
    log.critical("  \\____/_/  /_.___/_/\\__/\\__,_/_/  /___/_/ /_/\\__/\\___/_/   ")
    log.critical("")
    log.critical("##############################################################")
    log.critical("01001111 01110010 01100010 01101001 01110100 01100001 01101100")
    log.critical("01001111 01110010 01100010 01101001 01110100 01100001 01101100")
    log.critical("==============================================================")
    log.critical("")
    log.critical("                        Orbital Intel                         ")
    log.critical("                   QR Code VCard Generator                    ")
    log.critical("")
    log.critical("==============================================================")
    log.critical("01001111 01110010 01100010 01101001 01110100 01100001 01101100")
    log.critical("01001111 01110010 01100010 01101001 01110100 01100001 01101100")
    log.critical("##############################################################")
    log.critical("")
    log.critical(f'Copyright (c) {COPYRIGHT} Orbital Intelligence LLC')
    log.critical(f"Version {VERSION}")
    log.critical("")

    # Configure and Process command line arguments
    parser = argparse.ArgumentParser(description="ContactCardQRCodeGenerator - QR Code VCard Contact Card Generation Utility"
		, prog='ContactCardQRCodeGenerator.py'
		, formatter_class=RawTextHelpFormatter)

    parser.add_argument('configfile', help=f'Provide the configuration JSON file with contact card settings.')
    parser.add_argument('--destfile', '-df', default=DEFAULT_QRCODE_FILENAME, help=f'Set the destination filename for the generated QR code\nDefault is {DEFAULT_QRCODE_FILENAME}')
    parser.add_argument("--verbose",  "-v", action="store_true", help="Flag to display verbose output \nVerbose output is disabled by default")
    args = parser.parse_args()

    # Apply the verbose output setting
    if args.verbose:
        log.level=logging.DEBUG
        
    # Set the destination filename
    destFile = args.destfile
        
    # Set the configuration settings file
    configFile = args.configfile

    try:

        # Load config details
        objConfig = Config(configFile, destFile)  # Create and initialize Config class object

        # Get the current datetime
        startUtcDatetime = datetime.now(timezone.utc)
        startLocalDatetime = datetime.now()

        # Display program configuration data
        log.critical('')
        log.critical(f'Command line: {GetCommandLine()}')
        log.critical(f"QR Code File: {objConfig.destFile}")
        log.critical(f"Module Style: {objConfig.moduleStyle}")
        log.critical(f"Version/Size: {objConfig.versionSize}")
        log.critical(f"First Name:   {objConfig.firstName}")
        log.critical(f"Last Name:    {objConfig.lastName}")
        log.critical(f"Title:        {objConfig.title}")
        log.critical(f"Organization: {objConfig.organization}")
        log.critical(f"Phone:        {objConfig.phone}")
        log.critical(f"Email:        {objConfig.email}")
        log.critical(f"Url:          {objConfig.url}")
        log.critical(f"Front Color:  {objConfig.frontColorRed:3d} {objConfig.frontColorGreen:3d} {objConfig.frontColorBlue:3d}")
        log.critical(f"Back Color:   {objConfig.backColorRed:3d} {objConfig.backColorGreen:3d} {objConfig.backColorBlue:3d}")
        log.critical('')

        log.critical('Generating VCard Contact Card QR Code...')
        GenerateContactCard(objConfig)
        log.critical('Success')

    except KeyboardInterrupt:
        log.critical('')
        log.critical('#############################################')
        log.critical('ContactCardQRCodeGenerator.py aborted by user.')
        log.critical('#############################################')
        sys.exit(0)
    except Exception as error:
        log.critical('#############################################')
        log.critical('General Error during ContactCardQRCodeGenerator.py processing.')
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
        log.info(f'ContactCardQRCodeGenerator processing started at:   {startLocalDatetime}L / {startUtcDatetime}Z')
        log.info(f'ContactCardQRCodeGenerator processing completed at: {endLocalDatetime}L / {endUtcDatetime}Z')
        log.info('')
        log.critical(f'ContactCardQRCodeGenerator processing time:   {executionTime} ')
        log.critical('')
        log.critical(f'QR Code file: {os.path.join(baseDirectory, objConfig.destFile)}')
        log.critical(f'QR Code file: {os.path.join(baseDirectory, objConfig.destFileTimestamp)}')
        log.critical('')
        log.critical(f'Log file:     {LOG_FILENAME}')
        log.critical('')
        log.critical('######################################################')
        log.critical('ContactCardQRCodeGenerator completed.   ')
        log.critical('######################################################')


if __name__ == "__main__":
    main()



