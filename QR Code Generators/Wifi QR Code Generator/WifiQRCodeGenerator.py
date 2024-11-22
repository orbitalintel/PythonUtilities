#
# Orbital Intelligence Python Coding Samples 
#
# WifiQRCodeGenerator - Creates a QR code for automatically joining a WiFi network
#
# Copyright 2024 Orbital Intelligence LLC
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
COPYRIGHT = '2024'

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

    moduleStyleWifi = ''
    moduleStyleOnboarding = ''
    versionSize = 5
    border = 4

    wifiNetwork = ''
    wifiPassword = ''

    destFileWifi = ''

    sha256 = '' 
    sha1 = ''
    md5 = ''

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

        if (configData['config']['ModuleStyleWifi'].lower() == 'gappedsquare'):
            self.moduleStyleWifi = MODULE_DRAWER_STYLE_GAPPED_SQUARE
        elif (configData['config']['ModuleStyleWifi'].lower() == 'verticalbars'):
            self.moduleStyleWifi = MODULE_DRAWER_STYLE_VERTICAL_BARS
        elif (configData['config']['ModuleStyleWifi'].lower() == 'horizontalbars'):
            self.moduleStyleWifi = MODULE_DRAWER_STYLE_HORIZONTAL_BARS
        elif (configData['config']['ModuleStyleWifi'].lower() == 'rounded'):
            self.moduleStyleWifi = MODULE_DRAWER_STYLE_ROUNDED
        elif (configData['config']['ModuleStyleWifi'].lower() == 'square'):
            self.moduleStyleWifi = MODULE_DRAWER_STYLE_SQUARE
        else:
            self.moduleStyleWifi = MODULE_DRAWER_STYLE_SQUARE # This is the basic/standard QR code format

        self.destFileWifi = f'QR_Code_Wifi_{filenameDateTime}.png'

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

def GenerateWifiQRCode(config):
    # Create a QR Code object
    qrWifi = qrcode.QRCode(version=config.versionSize,
                           error_correction=qrcode.constants.ERROR_CORRECT_M,
                           border = config.border)

    # Prepare QR Code data
    qrWifi.add_data(f'WIFI:S:{config.wifiNetwork};T:WPA;P:{config.wifiPassword};H:false;;')

    # Generate QR Code using the specified style

    # Vertical Bars 
    if (config.moduleStyleWifi == MODULE_DRAWER_STYLE_VERTICAL_BARS):
        qr_img = qrWifi.make_image(image_factory=StyledPilImage,
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
    elif (config.moduleStyleWifi == MODULE_DRAWER_STYLE_HORIZONTAL_BARS):
        qr_img = qrWifi.make_image(image_factory=StyledPilImage,
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
    elif (config.moduleStyleWifi == MODULE_DRAWER_STYLE_GAPPED_SQUARE):
        qr_img = qrWifi.make_image(image_factory=StyledPilImage,
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
    elif (config.moduleStyleWifi == MODULE_DRAWER_STYLE_SQUARE):
        qr_img = qrWifi.make_image(image_factory=StyledPilImage,
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
    elif (config.moduleStyleWifi == MODULE_DRAWER_STYLE_ROUNDED):
        qr_img = qrWifi.make_image(image_factory=StyledPilImage,
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
    qr_img.save(os.path.join(baseDirectory, config.destFileWifi))

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
    log.critical("                WiFi Network QR Code Generator                ")
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
    parser = argparse.ArgumentParser(description="WifiQRCodeGenerator - WiFi Network QR Code Generation Utility"
		, prog='WifiQRCodeGenerator.py'
		, formatter_class=RawTextHelpFormatter)

    parser.add_argument('configfile', help=f'Provide the configuration JSON file with the Engagement settings.')
    parser.add_argument('network', default="", help=f'Set the WiFi network name (SSID).')
    parser.add_argument('password', default="", help=f'Set the Password for the WiFi network.')
    parser.add_argument("--verbose",  "-v", action="store_true", help="Flag to display verbose output \nVerbose output is disabled by default")
    args = parser.parse_args()

    # Apply the verbose output setting
    if args.verbose:
        log.level=logging.DEBUG

    # Set the configuration settings file
    configFile = args.configfile

    # Set the Wifi network name
    wifiNetwork = args.network

    # Set the Wifi password
    wifiPassword = args.password

    try:

        # Load config details
        objConfig = Config(configFile)  # Create and initialize Config class object
        objConfig.wifiNetwork = wifiNetwork
        objConfig.wifiPassword = wifiPassword

        # Get the current UTC date/time
        startUtcDatetime = datetime.now(timezone.utc)
        startLocalDatetime = datetime.now()

        # Display program configuration data
        log.critical('')
        log.critical(f'Command line:     {GetCommandLine()}')
        log.critical(f"QR Code File:     {objConfig.destFileWifi}")
        log.critical(f"Module Style E:   {objConfig.moduleStyleWifi}")
        log.critical(f"Module Style O:   {objConfig.moduleStyleOnboarding}")
        log.critical(f"Version/Size:     {objConfig.versionSize}")
        log.critical(f"Border:           {objConfig.border}")
        log.critical(f"Wifi Network:     {objConfig.wifiNetwork}")
        log.critical(f"Wifi Password:    {objConfig.wifiPassword}")
        log.critical(f"Front Color:      {objConfig.frontColorRed:3d} {objConfig.frontColorGreen:3d} {objConfig.frontColorBlue:3d}")
        log.critical(f"Back Color:       {objConfig.backColorRed:3d} {objConfig.backColorGreen:3d} {objConfig.backColorBlue:3d}")

        log.critical('')

        log.critical('Generating WiFi QR Code...')
        GenerateWifiQRCode(objConfig)
        log.critical('Success')

    except KeyboardInterrupt:
        log.critical('')
        log.critical('#############################################')
        log.critical('WifiQRCodeGenerator.py aborted by user.')
        log.critical('#############################################')
        sys.exit(0)
    except Exception as error:
        log.critical('#############################################')
        log.critical('General Error during WifiQRCodeGenerator.py processing.')
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
        log.info(f'WifiQRCodeGenerator processing started at:   {startLocalDatetime}L / {startUtcDatetime}Z')
        log.info(f'WifiQRCodeGenerator processing completed at: {endLocalDatetime}L / {endUtcDatetime}Z')
        log.info('')
        log.critical(f'WifiQRCodeGenerator processing time:   {executionTime} ')
        log.critical('')
        log.critical(f'WiFi QR Code file: {os.path.join(baseDirectory, objConfig.destFileWifi)}')
        log.critical('')
        log.critical(f'Log file: {LOG_FILENAME}')
        log.critical('')
        log.critical('######################################################')
        log.critical('WifiQRCodeGenerator completed.   ')
        log.critical('######################################################')


if __name__ == "__main__":
    main()



