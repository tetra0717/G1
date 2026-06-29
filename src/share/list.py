"""現在共有しているファイルの一覧を取得する。"""
import argparse


def add_list_parser(subparsers) -> None:
    """``share list`` サブコマンドを登録する."""
    parser = subparsers.add_parser("list", help="アップロードされたファイルの一覧を取得する")
    parser.set_defaults(func=cmd_list)

def cmd_list(args) -> int:
    """``share list`` コマンドのハンドラ."""
    from share.client import get_client

    dbx = get_client()
    if dbx is None:
        print("エラー: 認証が必要です。")
        print("'share auth' を実行してください。")
        return 1

    links = list_shared_links(dbx)
    if not links:
        print("共有リンクはまだありません。")
        return 0

    for link in links:
        print(f"{link['name']}\t{link['url']}")
    return 0

def list_shared_links(dbx) -> list[dict]:
    """Dropbox の共有リンクを全件返す。

    Args:
        dbx: dropbox.Dropbox インスタンス

    Returns:
        {"path": str, "url": str, "name": str} のリスト
    """
    links = []
    result = dbx.sharing_list_shared_links()
    while True:
        for link in result.links:
            links.append({
                "path": link.path_lower,
                "url": link.url,
                "name": link.name,
            })
        if not result.has_more:
            break
        result = dbx.sharing_list_shared_links(cursor=result.cursor)
    return links
