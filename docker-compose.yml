services:
  mysql:
    build:
      # context: Dockerfile을 빌드할 때 기준이 되는 디렉토리입니다.
      # COPY 명령어의 경로는 이 context 디렉토리를 기준으로 해석됩니다.
      # mysql/Dockerfile 안에 'COPY ./mysql/conf/my.cnf ...' 처럼 루트 기준 경로가 있어서 '.'(프로젝트 루트)로 설정합니다.
      context: .
      dockerfile: mysql/Dockerfile
    ports:
      - "3307:3306"
    volumes:
      - ./mysql/data:/var/lib/mysql
    networks:
      - app-network

  web:
    build:
      context: .
      dockerfile: web/Dockerfile
    ports:
      - "70:80"
    # depends_on: 이 서비스가 시작되기 전에 먼저 시작해야 할 서비스를 지정합니다.
    # web 컨테이너가 mysql 컨테이너보다 먼저 뜨는 것을 방지합니다.
    # 단, mysql 프로세스가 완전히 준비(ready)됐음을 보장하지는 않습니다. 순서만 보장합니다.
    depends_on:
      - mysql
    networks:
      - app-network

networks:
  app-network:
    # driver: bridge — 같은 호스트 안에서 컨테이너끼리 통신할 수 있는 가상 네트워크를 만듭니다.
    # 이 네트워크에 속한 컨테이너들은 서비스 이름(mysql, web)을 호스트명으로 서로 접근할 수 있습니다.
    # 예: web 컨테이너에서 mysql 컨테이너로 접속할 때 호스트명을 'mysql'로 사용합니다.
    driver: bridge