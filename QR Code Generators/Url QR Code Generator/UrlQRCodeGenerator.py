#
# Orbital Intelligence Python Coding Samples 
#
# UrlQRCodeGenerator - Creates a QR code for opening a URL in a web browser
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

EMPTY_STRING = ''
BASE_SPACE = '   '  # Used to insert 3 'spaces' into a string

class Config:
    frontColorRed = 0
    frontColorGreen = 0
    frontColorBlue = 0
    backColorRed = 0
    backColorGreen = 0
    backColorBlue = 0

    ModuleStyle = ''
    versionSize = 5
    border = 4

    url = ''

    destFileUrl = ''

    def __init__(self, configurationFile):
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
        self.border = configData['config']['Border']

        if (configData['config']['ModuleStyle'].lower() == 'gappedsquare'):
            self.ModuleStyle = MODULE_DRAWER_STYLE_GAPPED_SQUARE
        elif (configData['config']['ModuleStyle'].lower() == 'verticalbars'):
            self.ModuleStyle = MODULE_DRAWER_STYLE_VERTICAL_BARS
        elif (configData['config']['ModuleStyle'].lower() == 'horizontalbars'):
            self.ModuleStyle = MODULE_DRAWER_STYLE_HORIZONTAL_BARS
        elif (configData['config']['ModuleStyle'].lower() == 'rounded'):
            self.ModuleStyle = MODULE_DRAWER_STYLE_ROUNDED
        elif (configData['config']['ModuleStyle'].lower() == 'square'):
            self.ModuleStyle = MODULE_DRAWER_STYLE_SQUARE
        else:
            self.ModuleStyle = MODULE_DRAWER_STYLE_SQUARE # This is the basic/standard QR code format

        self.url = configData['config']['Url']
        self.destFileUrl = f'QR_Code_Url_{filenameDateTime}.png'

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

def GenerateUrlQRCode(config):
    # Create a QR Code object
    qrUrl = qrcode.QRCode(version=config.versionSize,
                          error_correction=qrcode.constants.ERROR_CORRECT_M,
                          border = config.border)

    # Prepare QR Code data
    qrUrl.add_data(f'{config.url}')

    # Generate QR Code 

    # Vertical Bars 
    if (config.ModuleStyle == MODULE_DRAWER_STYLE_VERTICAL_BARS):
        qr_img = qrUrl.make_image(image_factory=StyledPilImage,
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
    elif (config.ModuleStyle == MODULE_DRAWER_STYLE_HORIZONTAL_BARS):
        qr_img = qrUrl.make_image(image_factory=StyledPilImage,
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
    elif (config.ModuleStyle == MODULE_DRAWER_STYLE_GAPPED_SQUARE):
        qr_img = qrUrl.make_image(image_factory=StyledPilImage,
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
    elif (config.ModuleStyle == MODULE_DRAWER_STYLE_SQUARE):
        qr_img = qrUrl.make_image(image_factory=StyledPilImage,
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
    elif (config.ModuleStyle == MODULE_DRAWER_STYLE_ROUNDED):
        qr_img = qrUrl.make_image(image_factory=StyledPilImage,
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

    # Save QR Code file
    qr_img.save(os.path.join(baseDirectory, config.destFileUrl))


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
    log.critical("                    URL QR Code Generator                     ")
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
    parser = argparse.ArgumentParser(description="UrlQRCodeGenerator - QR Code Generation Utility for URLs"
		, prog='UrlQRCodeGenerator.py'
		, formatter_class=RawTextHelpFormatter)

    parser.add_argument('configfile', help=f'Provide the configuration JSON file with the URL settings.')
    parser.add_argument("--verbose",  "-v", action="store_true", help="Flag to display verbose output \nVerbose output is disabled by default")
    args = parser.parse_args()

    # Apply the verbose output setting
    if args.verbose:
        log.level=logging.DEBUG
        
    # Set the configuration settings file
    configFile = args.configfile

    try:
        # Load config details
        objConfig = Config(configFile)  # Create and initialize Config class object

        # Get the current datetime
        startUtcDatetime = datetime.now(timezone.utc)
        startLocalDatetime = datetime.now()

        # Display program configuration data
        log.critical('')
        log.critical(f'Command line:     {GetCommandLine()}')
        log.critical(f"QR Code File:     {objConfig.destFileUrl}")
        log.critical(f"Module Style:     {objConfig.ModuleStyle}")
        log.critical(f"Version/Size:     {objConfig.versionSize}")
        log.critical(f"Border:           {objConfig.border}")
        log.critical(f"Url:              {objConfig.url}")
        log.critical(f"Front Color:      {objConfig.frontColorRed:3d} {objConfig.frontColorGreen:3d} {objConfig.frontColorBlue:3d}")
        log.critical(f"Back Color:       {objConfig.backColorRed:3d} {objConfig.backColorGreen:3d} {objConfig.backColorBlue:3d}")
        log.critical('')

        log.critical('Generating URL QR Code...')
        GenerateUrlQRCode(objConfig)
        log.critical('Success')

    except KeyboardInterrupt:
        log.critical('')
        log.critical('#############################################')
        log.critical('UrlQRCodeGenerator.py aborted by user.')
        log.critical('#############################################')
        sys.exit(0)
    except Exception as error:
        log.critical('#############################################')
        log.critical('General Error during UrlQRCodeGenerator.py processing.')
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
        log.info(f'UrlQRCodeGenerator processing started at:   {startLocalDatetime}L / {startUtcDatetime}Z')
        log.info(f'UrlQRCodeGenerator processing completed at: {endLocalDatetime}L / {endUtcDatetime}Z')
        log.info('')
        log.critical(f'UrlQRCodeGenerator processing time:   {executionTime} ')
        log.critical('')
        log.critical(f'URL QR Code file: {os.path.join(baseDirectory, objConfig.destFileUrl)}')
        log.critical('')
        log.critical(f'Log file: {LOG_FILENAME}')
        log.critical('')
        log.critical('######################################################')
        log.critical('UrlQRCodeGenerator completed.   ')
        log.critical('######################################################')


if __name__ == "__main__":
    main()



