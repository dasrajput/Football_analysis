[Setup]
AppName=Football Analysis
AppVersion=1.0.0
AppPublisher= Dindayal Singh

DefaultDirName={pf}\Football Analysis
DefaultGroupName=Football Analysis
OutputBaseFilename=FootballAnalysisSetup
Compression=lzma
SolidCompression=yes
OutputDir=.\InstallerOutput
UninstallDisplayIcon={app}\Football Analysis.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: desktopicon; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "dist\Football Analysis\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Football Analysis"; Filename: "{app}\Football Analysis.exe"; IconFilename: "{app}\icon.ico"
Name: "{commondesktop}\Football Analysis"; Filename: "{app}\Football Analysis.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Registry]
Root: HKCU; Subkey: Software\DindayalSingh\Football Analysis; ValueType: string; ValueName: Install_Dir; ValueData: "{app}"; Flags: uninsdeletevalue