# batchPageSpeed（日本語）

`batchPageSpeed.py` は、複数のURLに対してGoogle LighthouseのPageSpeedデータをバッチで取得し、その結果をSQLiteデータベースに保存するPythonスクリプトです。このスクリプトは、非同期リクエストを使用してGoogle PageSpeed Insights APIからデータを取得し、実行ごとにタイムスタンプ付きのテーブルを自動で作成して結果を保存します。これにより、1日に複数回実行してもデータが重複せずに保存できます。また、SQLiteを使用しているため、データベースサーバーのセットアップは不要で、ローカルの軽量なデータベースで完結でき、簡単に結果を保存・管理できます。

### 解決されること

WEB版でPageSpeedデータを取得する場合、複数回実行するとそのたびに手動で待機し、処理が完了しているかを確認する必要があります。しかし、このスクリプトでは非同期処理を活用して、複数のURLを一度に効率よく処理できるため、待機時間を短縮し、手動で確認する手間を省けます。

## 機能

- 複数のURLに対して非同期でPageSpeedデータを取得。
- 結果をSQLiteデータベースに保存（データベースサーバー不要）。
- 各実行ごとにタイムスタンプに基づいた新しいデータベーステーブルを作成。
- 主要なパフォーマンス指標を取得：
  - パフォーマンススコア
  - アクセシビリティスコア
  - ベストプラクティススコア
  - SEOスコア
  - コアウェブバイタル（FCP, Speed Index, Interactive, FMP, CLS）

## セットアップ

1. **APIキーの取得**: Google PageSpeed InsightsのAPIキーを取得するには、[こちらの公式ドキュメント](https://developers.google.com/speed/docs/insights/v5/get-started?hl=ja)を参照してください。また、APIキーの取得方法について詳細が必要な場合は、[こちらの記事](https://zenn.dev/tmitsuoka0423/articles/get-gcp-api-key)も参考にしてください。

2. **`.env` ファイルの設定**: 取得したAPIキーを、プロジェクトのルートディレクトリに `.env` というファイルを作成し、以下のように記載してください：

   ```
   LIGHTHOUSE_API_KEY=your_api_key_here
   ```

3. **データベース設定**: デフォルトでは、結果は `/your_path/pagespeed_results.db` というSQLiteデータベースファイルに保存されます。SQLiteは軽量でローカルに保存できるため、データベースサーバーは必要ありません。必要に応じてスクリプト内でパスを変更してください。

## 使用方法

1. テストしたいURLを `urls_to_test` リストに追加します。

   ```python
   urls_to_test = [
       {"id": 1, "url": "https://example0.com/"},
       {"id": 2, "url": "https://example1.com/"},
       {"id": 3, "url": "https://example2.com/"},
   ]
   ```

2. スクリプトを実行すると、指定したURLに対して非同期でPageSpeedデータを取得し、結果がデータベースに保存されます。

```bash
python batchPageSpeed.py
```



<hr/>

# batchPageSpeed(English)

`batchPageSpeed.py` is a Python script that batch fetches Google Lighthouse PageSpeed data for multiple URLs and stores the results in an SQLite database. The script uses asynchronous requests to fetch data from the Google PageSpeed Insights API and automatically creates a timestamped table for each run to store the results. This allows you to run the script multiple times per day without data duplication. Additionally, since SQLite is used, there is no need for a database server, and everything can be done locally with a lightweight database, making it easy to save and manage results.

### What it solves

When fetching PageSpeed data via the web interface, if you run the process multiple times, you would need to manually wait for each run to complete and check if the process is finished. However, this script uses asynchronous processing to efficiently handle multiple URLs at once, reducing wait time and eliminating the need to manually check the process status.

## Features

- Asynchronously fetches PageSpeed data for multiple URLs.
- Saves results in an SQLite database (no database server required).
- Creates a new timestamp-based database table for each run.
- Fetches key performance indicators:
  - Performance score
  - Accessibility score
  - Best Practices score
  - SEO score
  - Core Web Vitals (FCP, Speed Index, Interactive, FMP, CLS)

## Setup

1. **Obtain an API Key**: To obtain a Google PageSpeed Insights API key, refer to [the official documentation here](https://developers.google.com/speed/docs/insights/v5/get-started?hl=ja). If you need more detailed instructions on how to obtain the API key, you can also refer to [this article](https://zenn.dev/tmitsuoka0423/articles/get-gcp-api-key).

2. **Configure the `.env` file**: After obtaining the API key, create a `.env` file in the root directory of your project and add the following:

   ```
   LIGHTHOUSE_API_KEY=your_api_key_here
   ```

3. **Database configuration**: By default, the results are saved in an SQLite database file located at `/your_path/pagespeed_results.db`. Since SQLite is lightweight and stores data locally, no database server is required. You can change the path in the script if necessary.

## Usage

1. Add the URLs you want to test to the `urls_to_test` list.

   Example:

   ```python
   urls_to_test = [
       {"id": 1, "url": "https://example0.com/"},
       {"id": 2, "url": "https://example1.com/"},
       {"id": 3, "url": "https://example2.com/"},
   ]
   ```

2. Run the script, and it will asynchronously fetch the PageSpeed data for the specified URLs and save the results to the database.

```bash
python batchPageSpeed.py
```

