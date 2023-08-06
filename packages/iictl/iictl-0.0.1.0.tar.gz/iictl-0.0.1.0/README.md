# iictl
cli를 통해 IntegratedInstance, pvc 등의 객체를 쉽게 생성/삭제하고 kubectl exec, kubectl cp를 binding하여 IntegratedInstance를 통해 접근 가능하도록 한다.

## 설치

```
pip install iictl
```

## instance

### create instance
```iictl run [options] 도커_이미지_이름 [커맨드]```

또는

```iictl run [options] 도커_이미지_이름 [-- 커맨드]```

도커 이미지 이름 뒤에도 옵션을 입력할 수 있다는 장점이 있다.

#### 옵션

|옵션|타입|설명|
|---|---|---|
|--name|str|이름을 지정할 수 있다. 지정하지 않을 경우 랜덤한 이름이 생성된다.|
|-e --env|str|key=value 형태의 environment variable. 여러번 사용이 가능하다.|
|-v --volume|str|volume:path 형태의 volume map. 여러번 사용이 가능하다.|
|--domain|str|port:domain 형태의 도메인 지정. domain은 *.kube.deep.est.ai 형태로 가능하다. 여러번 사용이 가능하다.|
|-w --workdir|str|container의 working dir 지정|

예시

```
iictl run --name=notebook -v notebook:/data -e TYPE=lab --domain 80:notebook.kube.deep.est.ai --workdir=/data caffeinism/pytorch-notebook -- jupyter blah blah ...
```

### delete instance
```iictl rm 인스턴스_이름```

```
iictl rm hello notebook ubuntu
```

### list instances
```iictl ps```

다음과 같은 형태로 출력된다.

```
name    image              status
------  -----------------  --------
hello   tutum/hello-world  Available
temp    busybox            Available
test    tutum/hello-world  Available
ubuntu  ubuntu             Available
```

### execute command in instance
```iictl exec [options] 인스턴스_이름 커맨드```

또는

```iictl exec [options] 인스턴스_이름 -- 커맨드```

|옵션|타입|설명|
|---|---|---|
|-t --tty|flag|TTY를 사용한다.|
|-i --stdin|flag|stdin을 사용한다.|

예시
```
iictl exec -it notebook -- bash
```

### view instance logs
```iictl logs [options] 인스턴스_이름```

|옵션|타입|설명|
|---|---|---|
|--tail|int|로그의 아래 tail줄만 출력한다.|
|-f --follow|flag|로그를 전부 출력하고 대기상태가 되며 이후 실행되어 추가된 로그도 계속 출력한다|

```
iictl logs --tail=100 -f notebook
```

### attach to instance
```iictl attach [options] 인스턴스_이름```

|옵션|타입|설명|
|---|---|---|
|-t --tty|flag|TTY를 사용한다.|
|-i --stdin|flag|stdin을 사용한다.|

예시
```
iictl attach -it notebook
```

## volume

### create volume

```iictl volume create 볼륨_이름 볼륨_크기```

볼륨 크기의 기본 단위는 byte이다.

|사용 가능 단위|
|-------------|
|Mi|
|Gi|
|Ti|

### delete volume

```iictl volume rm 볼륨_이름```

### list volume

```iictl volume ls```

### protect & unprotect volume
실수로 volume rm을 통해 volume을 삭제하지 않도록 한다.

```iictl volume protect 볼륨_이름```

```iictl volume unprotect 볼륨_이름```

## metric

### view gpu status
