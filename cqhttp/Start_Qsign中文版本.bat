@echo off
chcp 936 > NUL
title Qsign-Onekey �ػ�����
setlocal enabledelayedexpansion
set JAVA_HOME=.\jre
set "ver=2024-01-05"
set "library=txlib/"
set "config_file=config.yml"
set "account=1233456"
set "password="
set "author=rhwong shia kagangtuya-star"

if not exist "txlib_version.json" (
	REM txlib_version_config_file does not exist.
) else ( 
for /F "delims=" %%D in ('lib\jq.exe -r ".txlib_version" txlib_version.json') do set "txlib_version=%%D" 
)
set "json_file=%library%%txlib_version%/config.json"

echo -------------------------------------------------------------------------------------------------
echo * ______  ______  __  ______  __   __       ______  __   __  ______  __  __  ______  __  __    *
echo */\  __ \/\  ___\/\ \/\  ___\/\ \-.\ \     /\  __ \/\ \-.\ \/\  ___\/\ \/ / /\  ___\/\ \_\ \   *
echo *\ \ \/\_\ \___  \ \ \ \ \__ \ \ \-.  \    \ \ \/\ \ \ \-.  \ \  __\\ \  _'-\ \  __\\ \____ \  *
echo * \ \___\_\/\_____\ \_\ \_____\ \_\\ \_\    \ \_____\ \_\\ \_\ \_____\ \_\ \_\ \_____\/\_____\ *
echo *  \/___/_/\/_____/\/_/\/_____/\/_/ \/_/     \/_____/\/_/ \/_/\/_____/\/_/\/_/\/_____/\/_____/ *
echo -------------------------------------------------------------------------------------------------
                                                                                              
if not exist "txlib_version.json" (
  echo -------------------------------------------------------------------------------------------------
  echo unidbg-fetch-qsign-onekey Ver.%ver% by %author%
  echo [txlib_version.json] �汾��Ϣ�ļ�δ�ҵ���
  echo ������Ҫ�趨��ѡ��,��Enter��ȷ�ϡ�
  echo �����ֱ�Ӱ���Enter�������ᱣ����ʾ��Ĭ�ϲ�����
  echo -------------------------------------------------------------------------------------------------
  set /p "txlib_version=txlib�汾(Ĭ��:8.9.88): "
       if "!txlib_version!"=="" (
	   set "txlib_version=8.9.88"
       )  
  set "json_file=%library%!txlib_version!/config.json"
  
  set /p "host=����IP[HOST](Ĭ��:127.0.0.1): "
      if "!host!"=="" (
      set "host=127.0.0.1"
      )
  set /p "port=�˿�[PORT](Ĭ��:13579): "
      if "!port!"=="" (
      set "port=13579"
      )
  set /p "key=��Կ[KEY](Ĭ��:1145141919810): "
      if "!key!"=="" (
      set "key=1145141919810"
      )

if not exist "txlib\!txlib_version!\" (
  echo -------------------------------------------------------------------------------------------------
      echo ���棡����� txlib �汾�š�
      echo ���� "txlib" �ļ���!
      echo ��������Ŀǰ�Ѿ���װ�� txlib �汾��:
      dir txlib /b /ad
  echo -------------------------------------------------------------------------------------------------
      timeout 10
      exit /b
  ) else (
      for /F "delims=" %%P in ('lib\jq.exe -r ".protocol.package_name" !json_file!') do set "p_package_name=%%P"
      for /F "delims=" %%Q in ('lib\jq.exe -r ".protocol.qua" !json_file!') do set "p_qua=%%Q"
      for /F "delims=" %%V in ('lib\jq.exe -r ".protocol.version" !json_file!') do set "p_version=%%V"
      for /F "delims=" %%O in ('lib\jq.exe -r ".protocol.code" !json_file!') do set "p_code=%%O"
        echo { "server": { "host": "!host!", "port": !port! }, "share_token": false, "count": 5, "key": "!key!", "auto_register": true, "protocol": { "package_name": "!p_package_name!", "qua": "!p_qua!", "version": "!p_version!", "code": "!p_code!" }, "unidbg": { "dynarmic": false, "unicorn": true, "kvm": false, "debug": false } } > "!json_file!"
        echo {"txlib_version": "!txlib_version!"} > txlib_version.json
  )

) else (   
  for /F "delims=" %%D in ('lib\jq.exe -r ".txlib_version" txlib_version.json') do set "txlib_version=%%D"
  set "json_file=%library%!txlib_version!/config.json"
  echo -------------------------------------------------------------------------------------------------
  echo unidbg-fetch-qsign-onekey Ver.%ver% by %author%
  echo txlib �汾��Ϊ %txlib_version%
  echo �������Ҫ�޸� txlib �汾�� , ��ɾ�� [txlib_version.json] �ļ�!
  echo -------------------------------------------------------------------------------------------------
  for /F "delims=" %%A in ('lib\jq.exe -r ".server.host" %json_file%') do set "host=%%A"
  for /F "delims=" %%B in ('lib\jq.exe -r ".server.port" %json_file%') do set "port=%%B"
  for /F "delims=" %%C in ('lib\jq.exe -r ".key" %json_file%') do set "key=%%C"
)

set "targetPattern=*go-cqhttp*.exe"
set "fileExists=0"

for %%i in (%targetPattern%) do (
    set "fileExists=1"
)

if %fileExists%==1 (
  if exist "%config_file%" (
    lib\sed.exe -i "s/url: 'http:\/\/127.0.0.1:8080'/Example-sign-server/; s/url: 'https:\/\/signserver.example.com'/Example-sign-server/" "%config_file%"
    if "!host!"=="0.0.0.0" (
      lib\sed.exe -i "0,/url: '.*'/s/url: '.*'/url: 'http:\/\/localhost:!port!'/; 0,/key: '.*'/s/key: '.*'/key: '!key!'/" "%config_file%"
      ) else ( 
      lib\sed.exe -i "0,/url: '.*'/s/url: '.*'/url: 'http:\/\/!host!:!port!'/; 0,/key: '.*'/s/key: '.*'/key: '!key!'/" "%config_file%"
      )
  ) else (
    echo û�ҵ�go-cqhttp�������ļ� [config.yml]. ����������������������� [go-cqhttp.bat] 
  )
      echo ͬ����ǰ txlib �汾Э���ļ���go-cqhttp��Э����ϢĿ¼.
      md data\versions
      if "!txlib_version!" neq "3.5.1" (
        if "!txlib_version!" neq "3.5.2" (
			if "!txlib_version!" neq "3.5.5" (
				if "!txlib_version!" neq "5.8.2" (
      copy txlib\!txlib_version!\android_pad.json data\versions\6.json
      copy txlib\!txlib_version!\android_phone.json data\versions\1.json
				)
			)
        )
      )
) else (
  echo �� go-cqhttp ��������?
  echo ��ע���ֶ�ͬ���汾Э���ļ���go-cqhttp��Э����ϢĿ¼��
  echo Ȼ������ Qsign API ��ַ�� KEY ����Ӧ�Ŀͻ����С�
)  
  findstr /C:"uin: 1233456" "%config_file%" 2>nul >nul
  if %errorlevel% equ 0 (
      set /p "account=�ʺ�: "
      set /p "password=����: "
      echo -------------------------------------------------------------------------------------------------
      echo ����ʺ�:!account! ����:!password!
      lib\sed.exe -i "s/uin: 1233456/uin: !account!/g; s/password: ''/password: '!password!'/g; s/auto-refresh-token: false/auto-refresh-token: true/g" "%config_file%"
      echo �ʺź�������Ϣ�ѱ���!
  ) else (
      echo -------------------------------------------------------------------------------------------------
      echo �ļ� [config.yml] ���Ѱ����ʻ���Ϣ���߸��ļ������ڣ�
      echo �����ʻ���Ϣ���á�
  )

echo -------------------------------------------------------------------------------------------------
echo Qsign API ��ַ:http://!host!:!port!
echo ��Կ KEY=!key!
echo Qsign-Onekey�汾:%ver%
echo TXlib�汾:%txlib_version% 
echo -------------------------------------------------------------------------------------------------
timeout /t 3 > nul

where curl >nul 2>nul
echo ���ϵͳ���Ƿ��Ѱ�װCurl...
if %errorlevel% equ 0 (
  echo ��⵽curl�����ʹ��ϵͳ������curl�������С�
  set "curl_command=curl"
) else (
  echo δ��⵽curl�����ʹ��һ�����Դ��� "curl.exe" �������С��˱������x86_64ϵͳʹ�á�
  set "curl_command=lib\curl.exe"
)

:loop
if "!host!"=="0.0.0.0" (
       set "core_host=localhost"
      ) else ( 
      set "core_host=!host!"
      )
%curl_command% -I http://!core_host!:!port!/register?uin=12345678 --connect-timeout 5 -m 5 >nul 2>nul
if %errorlevel% equ 0 (
    echo Qsign API ��
    timeout /t 30 /nobreak >nul
    goto loop
) else (
    echo Qsign API ̽��ʧ�ܣ����ڽ������̲���������...
    if defined pid (
      tasklist /fi "PID eq !pid!" | findstr /i "!pid!" >nul
        if %errorlevel% equ 0 (
          taskkill /F /PID !pid!))
    start "Qsign-Onekey ���Ľ���" cmd /c "bin\unidbg-fetch-qsign --basePath=%library%%txlib_version%"
    timeout /t 15 /nobreak >nul
    for /f "tokens=5" %%A in ('netstat -ano ^| findstr ":!port!.*LISTENING"') do (
      set "pid=%%A")
    echo Qsign API ������ PID:!pid!
    goto loop
)
