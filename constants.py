import os

UI_DIR = os.path.join(os.path.dirname(__file__), "UIs")

SUBCATEGORIES = {
    "Education": [
        ("Art", "Art"),
        ("Construction", "Construction"),
        ("Music", "Music"),
        ("Languages", "Languages"),
        ("ArtificialIntelligence", "Artificial Intelligence"),
        ("Astronomy", "Astronomy"),
        ("Biology", "Biology"),
        ("Chemistry", "Chemistry"),
        ("ComputerScience", "Computer Science"),
        ("DataVisualization", "Data Visualization"),
        ("Economy", "Economics"),
        ("Electricity", "Electricity"),
        ("Geography", "Geography"),
        ("Geology", "Geology"),
        ("Geoscience", "Geoscience"),
        ("History", "History"),
        ("Humanities", "Humanities"),
        ("ImageProcessing", "Image Processing"),
        ("Literature", "Literature"),
        ("Maps", "Maps"),
        ("Math", "Math"),
        ("NumericalAnalysis", "Numerical Analysis"),
        ("MedicalSoftware", "Medical Software"),
        ("Physics", "Physics"),
        ("Robotics", "Robotics"),
        ("Spirituality", "Spirituality"),
        ("Sports", "Sports"),
        ("ParallelComputing", "Parallel Computing")
    ],

    "Game": [
        ("ActionGame", "Action"),
        ("AdventureGame", "Adventure"),
        ("ArcadeGame", "Arcade"),
        ("BoardGame", "Board"),
        ("BlocksGame", "Blocks"),
        ("CardGame", "Cards"),
        ("KidsGame", "Kids"),
        ("LogicGame", "Logic"),
        ("RolePlaying", "RPGs"),
        ("Shooter", "Shooters"),
        ("Simulation", "Simulation"),
        ("SportsGame", "Sports"),
        ("StrategyGame", "Strategy")
    ],

    "Graphics": [
        ("2DGraphics", "2D Graphics"),
        ("VectorGraphics", "Vector Graphics"),
        ("RasterGraphics", "Raster Graphics"),
        ("3DGraphics", "3D Graphics"),
        ("Scanning", "Scanning"),
        ("OCR", "OCR"),
        ("Photography", "Photography"),
        ("Publishing", "Publishing"),
        ("Viewer", "Viewer")
    ],

    "Network": [
        ("InstantMessaging", "Instant Messaging"),
        ("Chat", "Chatting"),
        ("IRCClient", "IRC Clients"),
        ("Feed", "Feed Readers"),
        ("FileTransfer", "File Transfers"),
        ("HamRadio", "Ham Radio"),
        ("News", "News"),
        ("P2P", "P2P"),
        ("RemoteAccess", "Remote Access"),
        ("Telephony", "Telephony"),
        ("VideoConference", "Video Conference"),
        ("WebBrowser", "Web Browser")
    ],

    "Office": [
        ("Calendar", "Calendars"),
        ("ContactManagement", "Contact Management"),
        ("Database", "Databases"),
        ("Dictionary", "Dictionaries"),
        ("Chart", "Charts"),
        ("Email", "Email"),
        ("Finance", "Finance"),
        ("FlowChart", "Flow Chart"),
        ("PDA", "PDA"),
        ("ProjectManagement", "Project Management"),
        ("Presentation", "Presentations"),
        ("Spreadsheet", "Spreadsheets"),
        ("WordProcessor", "Word Processors")
    ],

    "Utility": [
        ("TextTools", "Text Tools"),
        ("Calculator", "Calculators"),
        ("Clock", "Clocks"),
        ("TextEditor", "Text Editors"),
        ("FileTools", "File Tools"),
        ("Accessibility", "Accessibility"),
        ("ConsoleOnly", "Terminal Apps")
    ],

    "Video": [
        ("Player", "Video Players"),
        ("Recorder", "Video Recording"),
        ("AudioVideoEditing", "Video Editing"),
        ("TV", "TV"),
        ("DiscBurning", "Disc Burning")
    ],

    "System": [
        ("DesktopSettings", "Desktop Settings"),
        ("HardwareSettings", "Hardware Settings"),
        ("Printing", "Printing"),
        ("PackageManager", "Package Managers"),
        ("FileManager", "File Managers"),
        ("TerminalEmulator", "Terminal Emulators"),
        ("Filesystem", "Filesystem"),
        ("Monitor", "Monitoring"),
        ("Security", "Security"),
        ("Accessibility", "Accessibility")
    ]
}