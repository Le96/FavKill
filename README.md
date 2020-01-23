# FavKill
Make your twitter account clean. No more Fav-Digger.

# 使い方
## 依存関係
- Python 3系
- Pipenv

## Twitter Developers 登録
[Twitter Developers](https://developer.twitter.com/) にてTwitter開発者アカウントを登録する。
[kngsym2018氏のQiita記事](https://qiita.com/kngsym2018/items/2524d21455aac111cdee "Twitter API 登録 \(アカウント申請方法\) から承認されるまでの手順まとめ")などが詳しい。
すでにアカウントを所持している場合はこのステップをスキップする。

## Twitter Application 登録
<https://developer.twitter.com/en/apps> にてTwitterアプリケーションを登録する。
画面右上の`Create an app`ボタンを押すことでアプリケーションを登録できる。
各パラメータは任意に記入する。
`(required)`と記されたパラメータについては必須。

`Allow this application to be used to sign in with Twitter`の項目には*`Enable Sign in with Twitter`にチェックを入れる*。
加えて`Callback URLs`には*`http://127.0.130.96:13096`を記入する*。

## Keys and tokens
作成したアプリケーションの認証情報を取得する。
- 当該アプリケーション右側`Details`をクリック
- 画面上部`Keys and tokens`をクリック
- `Consumer API keys`の`API key`, `API secret key`を取得
  - `./sample_env/credentials/consumer.py`の`CONSUMER_KEY`, `CONSUMER_SECRET`をそれぞれ置換
- `Access token & access token secret`右側の`Generate`をクリック
- ポップアップの`Access token`, `Access token secret`を取得
  - この画面を抜けると再取得できず、*再生成するしかなくなるので注意*
  - `./sample_env/credentials/access_token.py`の`sampleuser`部分を自分(Twitter開発者アカウントとして扱っているアカウント)のscreen nameで置換
  - `KEY`, `SECRET`部分をそれぞれ置換

また、当該アカウント以外の認証情報(`Access token`, `Access token secret`)は次のステップにて取得できる。

## 開発者アカウント以外の認証情報取得
`$ ./acquire_token.py`を実行する。

## TODO これ以降を書く
