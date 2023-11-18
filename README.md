

### 2.2 ECRに独自のイメージをpush

イメージの作成
```shell
# サービスごとにイメージ名を直接しているす
docker compose build
```

ECRにログイン
```shell
aws ecr get-login-password --region ap-northeast-1 --profile <名前を変える> | docker login --username AWS --password-stdin <AWSアカウントID>.dkr.ecr.ap-northeast-1.amazonaws.com
```

タグを設定
```shell
docker tag <image名>:latest <AWSアカウントID>.dkr.ecr.ap-northeast-1.amazonaws.com/<image名>:latest
```

ECRにpush
```shell
docker push <AWSアカウントID>.dkr.ecr.ap-northeast-1.amazonaws.com/<image名>:latest
```

---

### 2.3 ECSデプロイ用のdocker-compose.ymlを作成
**docker-compose-ecs-deploy.yml**とし*imageをECRのものに変更*

---


## 3. docker context ecsの作成

ecsコンテキストを作成していないなら作る
```shell
docker context create ecs <名前>
```

ecsコンテキストを切り替え
```shell
docker context use <名前>
```

ECS fargateにpush
```shell
docker compose -f docker-compose-ecs-deploy.yml up
```

ecsコンテキストをdefaultに戻す
```shell
docker context use default
```

---

## 4. ECS Fargateのデプロイ先のリージョンが合わない時
```shell
# aws configure set test-dym.region ap-northeast-1
aws configure set <プロファイル>.region ap-northeast-1
```

---

## 5. AWS Fargateでコンテナに接続

### 5.1 コンソール画面での初期設定
[ECS TaskにIAMロールを付与することができるようになりました](https://dev.classmethod.jp/articles/20160715-ecs-task-iam-role/#toc-5)

[ECS execでFargateのコンテナにアクセスする方法](https://memomaru.life/access-to-fargate-container-ecs-exec/)
1. Task定義で新しいリビジョンを作成する
2. その際に他の設定はデフォルトのままで、タスクロールを**ecsExecCommandRole**にする
3. clusterからサービスを選択し、先ほど作成したリビジョンに変更して更新をかける


### 5.2 サービスの更新
サービスの更新
```shell
aws ecs update-service --cluster <クラスター名> --service <サービス名> --enable-execute-command --profile <プロファイル> --region ap-northeast-1
```

### 5.3 コンテナへ接続

```shell
aws ecs execute-command --cluster <クラスター名> --task <タスク名> --container <コンテナ名> --interactive --profile <プロファイル> --region ap-northeast-1 --command "ls"
```
---

## 6. 使いたい機能
<ul>
<li style="color: powderblue">FastApi</li>
<li style="color: powderblue">GraphQL</li>
<li style="color: powderblue">Athena, QuickSight, DynamoDB</li>

</ul>

---

### 7. 良い記事

[docker-compose.ymlを使って WordpressをAWSFargateへデプロイ](https://tech.kurojica.com/archives/57856/)

[Reactアプリをdocker composeとECS(Fargate)でデプロイする](https://zenn.dev/maximum_maximum/articles/31c09e1b0f9491)

---

### 8. ローカルで確認URL
[フロントエンド: http://localhost/](http://localhost/)

[Django管理画面: http://localhost/admin](http://localhost/admin)

[DjangoのAPI: http://localhost/](http://localhost/api)

---

### 9. ライブラリをpipでinstallした場合
pipでpythonライブラリをインストールした場合<br>
requirements.txtにも反映しないといけない。下記を実行する
```shell
sh /tmp/lib-update.sh
```

---

### 10. AWS lambdaでレイヤーを作るときの注意点
OSによってライブラリの構築が変わってくるので、<br>
**pip install -r requirements.txt -t python**<br>
このコマンドを打つ時はコンテナイメージを下記イメージに合わせる<br>
**FROM public.ecr.aws/lambda/python:3.11**<br>
```dockerfile
FROM public.ecr.aws/lambda/python:3.11

# pycファイル(および__pycache__)の生成を行わないようにする
ENV PYTHONDONTWRITEBYTECODE=1
# 標準出力・標準エラーのストリームのバッファリングを行わない
ENV PYTHONUNBUFFERED=1
# コンテナのワークディレクトリを/codeに指定
WORKDIR ${LAMBDA_TASK_ROOT}

COPY --chmod=777 ./container/python/entrypoint.sh /tmp/entrypoint.sh
COPY --chmod=777 ./container/python/lib-update.sh /tmp/lib-update.sh
COPY ./container/python/requirements.txt /tmp/requirements.txt

# コンテナ内でpipをアップグレード
RUN pip install --upgrade pip

# pip install -r requirements.txtを実行
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY ./source ${LAMBDA_TASK_ROOT}

CMD ["index.handler"]


```

このイメージ上で、下記コマンドを実行する
```shell
docker compose exec python bash
mkdir python
pip install -r requirements.txt -t python
exec
mv python/python ~/Desktop
cd ~/Desktop
zip -r layer.zip python
```

出来上がったlayer.zipでレイヤーを作成

---

