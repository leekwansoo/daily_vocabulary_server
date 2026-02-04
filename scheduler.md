# Task Scheduler Commands in Power Shell  "schtasks"

help  

schtasks /query /?

설명:
    관리자가 로컬 또는 원격 시스템의 예약된 작업을
    표시할 수 있도록 합니다.

매개 변수 목록:
    /S    system         연결할 원격 시스템을 지정합니다.

    /U    username       schtasks.exe를 실행할 사용자 컨텍스트를
                         지정합니다.

    /P    [password]     제공된 사용자 컨텍스트에 대한
                         암호를 지정합니다. 생략된 경우 입력하도록 묻습니다.

    /FO   format         출력이 표시될 형식을 지정합니다.
                         유효한 값: TABLE, LIST, CSV.

    /NH                  출력에 열 머리글이 표시되지 않도록
                         지정합니다.
                         TABLE 및 CSV 형식에만 유효합니다.

    /V                   자세한 작업 출력을 표시합니다.

    /TN   taskname       정보를 검색할 작업의 경로\이름을
                         지정하거나 모두 지정합니다.

    /XML  [xml_type]     작업 정의를 XML 형식으로 표시합니다.

                         xml_type이 ONE이면 출력은 유효한 XML 파일 하나입니다.

                         xml_type이 없으면 출력은

                         모든 XML 작업 정의에 대한 연결입니다.

    /HRESULT             진단성 향상을 위해 프로세스 종료 코드는
                         HRESULT 형식이 됩니다.

    /?                   이 도움말 메시지를 표시합니다.

예:
    SCHTASKS /Query
    SCHTASKS /Query /?
    SCHTASKS /Query /S system /U user /P password
    SCHTASKS /Query /FO LIST /V /S system /U user /P password
    SCHTASKS /Query /FO TABLE /NH /V

    schtasks /query /tn "VocabularyViewTrigger" /fo LIST /v

## Solutions for keeping Streamlit running:

### Option 1: Using batch file (keeps terminal visible) - RECOMMENDED
schtasks /create /tn "StreamlitApp" /tr "C:\Users\user2\Desktop\daily_vocabulary_service-main\run_streamlit.bat" /sc daily /st 20:50 /f

### Option 2: Using cmd with /K flag + full path to file - SIMPLEST
schtasks /create /tn "StreamlitApp" /tr "cmd /K C:\Users\user2\AppData\Local\Programs\Python\Python313\Scripts\streamlit.exe run C:\Users\user2\Desktop\daily_vocabulary_service-main\trigger.py" /sc daily /st 21:15 /f

### Option 3: Using PowerShell (keeps window open)
schtasks /create /tn "StreamlitApp" /tr "powershell -NoExit -Command \"cd 'C:\Users\user2\Desktop\daily_vocabulary_service-main'; & 'C:\Users\user2\AppData\Local\Programs\Python\Python313\Scripts\streamlit.exe' run trigger.py\"" /sc daily /st 20:50 /f

### Original (terminal closes immediately - NOT RECOMMENDED)
schtasks /create /tn "StreamlitApp" /tr "C:\Users\user2\AppData\Local\Programs\Python\Python313\Scripts\streamlit.exe run app.py" /sc daily /st 20:50  /f