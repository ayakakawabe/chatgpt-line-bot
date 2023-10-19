# chatgpt-line-bot
ChatGPTが返信するLINEbot

ngrokでwebhookを設定し、PythonにLINEユーザの送信内容を送る。
それをChatGPTに投げて返信を作成してもらい、LINEに送り返す。

![システム構成イメージ](https://github.com/ayakakawabe/chatgpt-line-bot/assets/103473179/8352e9fc-9ad7-4e81-8873-55d8d8a133f4)

## 実行方法

ローカル環境での実行方法

### LINE Developersの設定
[Messaging API](https://developers.line.biz/ja/docs/messaging-api/getting-started/) でチャネルを作成し、チャネルアクセストークンとチャネルシークレットを取得する

### パッケージインストール

```
$ pip install flask
$ pip install line-bot-sdk
$ pip install python-dotenv
```

### .envの作成

ルートディレクトリに.envを作成する

```
CHANNEL_ACCESS_TOKEN='YOUR_CHANNEL_ACCESS_TOKEN'
CHANNEL_SECRET='YOUR_CHANNEL_SECRET'
OPENAI_API_KEY='YOUR_OPENAI_API_KEY'
```

'YOUR_CHANNEL_ACCESS_TOKEN'と'YOUR_CHANNEL_SECRET'を、Messaging API で取得したチャネルアクセストークンとチャネルシークレットに変更する

'YOUR_OPENAI_API_KEY'をOpenAIのAPIキーに変更する

### localhostの起動
```
$ export FLASK_APP=app.py
$ export FLASK_DEBUG=1
$ flask run --host=0.0.0.0
```

（サーバーが立ち上がっているか確認するために http://localhost:5000/ にアクセス → hello world!が表示されるか確認する）

### webhookの設定

[ngrok](https://ngrok.com/) でローカル環境を外部公開する
```
$ ngrok http 5000
```

Messaging APIのwebhook設定にngrokで取得したURL+'/callback'を入力する

Ex.)https://XXXXXXXX.ngrok-free.app/callback

### 実行

Messaging API のQRコードからLINEで友達追加して操作する

## 参考資料

* [Messaging API](https://developers.line.biz/ja/docs/messaging-api/getting-started/)
* [ngrok](https://ngrok.com/)
* [Qiita：Python（Flask）で作るLINE bot（＋ngrokで公開する方法）](https://qiita.com/ayakaintheclouds/items/6515a329d7cce94f8358)
