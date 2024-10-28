# Pour utiliser cette fonction,il faut péparer un trajectoire.csv,qui a copirs le ROSTopic de /tf au minimum(normalement /tf et /tf_static)

- Changer les répertoires de le fichier CSV et le fichier Lanelet2

- Si vous avez vue des problème de lancement, ça peut etre la version de VecterMap est update ou inUpdate   
  dans ce  cas là, contactez moi svp, pour le code adaptation à ta version de VectorMap.  
  (Maintenant le code est braché sur la verion Oct/2024 donc son format est comme ça:

  <node id="1" lat="46.12982337722" lon="-1.0794278177">
    <tag k="local_x" v="48365.1015"/>
    <tag k="local_y" v="10264.8907"/>
    <tag k="ele" v="53.9878"/>
  </node>

  l'ancienne version Aug/2024 est dans la format:

  <node id="48" lat="48.72244562283628" lon="2.257069031480778">
    <tag k="mgrs_code" v="31UDP453968"/>
    <tag k="local_x" v="45359.0525"/>
    <tag k="local_y" v="96868.3611"/>
    <tag k="ele" v="129.5001"/>
  </node>
  
  )
