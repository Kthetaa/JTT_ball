# JTT_ballの概要
graph.pngがJTTのボールの木です. graph.txtから生成されていて, これを編集すればgraph.pngの木が更新されます.
make_graph.pyは気にしなくていいです. AIが書いたので自分も中身がわかりません.

# graph.txtの仕様
a:b c  
のように書くと頂点aから頂点b,cにそれぞれ矢印を伸ばします.  
スペースで頂点を区切っているので頂点の名前にスペースは使用せず, "_"を使用してください.  
  
例えば頂点a,bから頂点cに矢印を伸ばすときは  
a:c  
b:c  
のように書くとできます.

# gitの使い方
(自分も初めて使うので最低限の知識しかありません)  
graph.txtを開いて右上の"Edit this file"のボタンを押すと編集できます.  
編集が完了したら右上の"Commit changes"のボタンを押し, メモ欄のところに変更点を軽く書いてください.  
"Commit changes", "Propose change", "Create pull request"×2の順にボタンを押して変更をリクエストすれば完了です.
あとは自分が反映させます.
