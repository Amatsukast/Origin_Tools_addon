import bpy

translation_dict = {
    "ja_JP": {
        ("*", "Move Origin"): "原点を移動",
        ("*", "Axis"): "軸",
        ("*", "The axis along which to move the origin."): "原点を移動する軸",
        ("*", "To Min"): "Min側へ",
        ("*", "Move origin to minimum side."): "原点を最小側に移動します",
        ("*", "Use Global Axis"): "グローバル軸を使用",
        (
            "*",
            "Use global coordinates instead of local.",
        ): "ローカル座標ではなくグローバル座標を使用します",
        ("*", "Move Origin to Center"): "原点を中心に移動",
        (
            "*",
            "The axis along which to center the origin.",
        ): "原点を中心に移動する軸",
        ("*", "Move Origin to Center (All Axes)"): "原点を全軸の中心に移動",
        (
            "*",
            "Move the origin to the bounding box center or center of mass of the selected mesh objects.",
        ): "選択メッシュのバウンディングボックス中心または重心に原点を移動します",
        ("*", "Axis Mode"): "軸の基準",
        ("*", "Axis reference."): "軸の基準",
        ("*", "Center Before Move"): "事前センタリング",
        (
            "*",
            "Center origin on all axes before moving to specified position.",
        ): "全軸センタリングしてから指定位置に移動します",
        ("*", "Move Mesh"): "メッシュを移動",
        (
            "*",
            "Move mesh instead of origin to match the specified position.",
        ): "原点を固定したまま、メッシュを移動して指定位置に合わせます",
        ("*", "Origin Tools"): "Origin Tools",
        ("*", "{0} axis:"): "{0}軸：",
        ("*", "Min"): "Min側",
        ("*", "Max"): "Max側",
        ("*", "Center"): "中心",
        ("*", "All Axes:"): "全軸：",
        ("*", "Center (All Axes)"): "中心に移動",
    }
}


def register(name):
    bpy.app.translations.unregister(name)
    bpy.app.translations.register(name, translation_dict)


def unregister(name):
    bpy.app.translations.unregister(name)
