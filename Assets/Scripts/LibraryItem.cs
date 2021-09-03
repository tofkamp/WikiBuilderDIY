using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LibraryItem      // : MonoBehaviour ?????
{
    
    public Vector3 centroid;     // point for rotation
    private List<ConnectorItem> connectors = new List<ConnectorItem>();
    
    public string name;
    private Mesh mesh;
    private int instanceCounter;
    private Texture2D icon = null;
    //public int thickness;

    

    public LibraryItem(LibraryItemJSON libitemjson) {
        const float scale = 1000f;

        this.centroid = new Vector3(libitemjson.centroid[0], libitemjson.centroid[1], libitemjson.centroid[2]) / scale;
        this.name = libitemjson.name;
        this.instanceCounter = 0;
        
        int connectorid = 0;
        foreach(ConnectorItemJSON conjson in libitemjson.connectors2) {
            this.connectors.Add(new ConnectorItem(conjson,connectorid));
            connectorid++;
        }
    
        List<Vector3> newVertices = new List<Vector3>();
        //List<Vector3> normals = new List<Vector3>();

        foreach(float[] vert in libitemjson.vertices) {
            newVertices.Add(new Vector3(vert[0],vert[1],vert[2]) / scale);
        }
        int nrVertices = newVertices.Count;
        List<int> newTriangles = new List<int>();
        foreach(int[] face in libitemjson.faces) {
            if (face.Length == 3) {
                newTriangles.Add(face[0]);
                newTriangles.Add(face[1]);
                newTriangles.Add(face[2]);
            }
            if (face.Length == 4) {   // quads are used for sideways, to have square shapes in unity, double vertices
                newTriangles.Add(face[0] + nrVertices);
                newTriangles.Add(face[1] + nrVertices);
                newTriangles.Add(face[2] + nrVertices);
            
                newTriangles.Add(face[0] + nrVertices);
                newTriangles.Add(face[2] + nrVertices);
                newTriangles.Add(face[3] + nrVertices);
            }
        }
        newVertices.AddRange(newVertices);
        this.mesh = new Mesh();
        this.mesh.SetVertices(newVertices);
        //this.mesh.SetNormals(normals);
        this.mesh.triangles = newTriangles.ToArray();
        this.mesh.RecalculateNormals();
        this.mesh.name = libitemjson.name;
    }

    public Texture2D getIcon(Camera snapshotCamera,Material objectMaterial) {
        /// <summary>
        /// make icons from objects, so a user can select them in the game
        /// </summary>
        if (this.icon == null) {
            Vector3 snapshotPos = new Vector3(-5,1,0);
            
            int resWidth = 128;
            int resHeight = 128;

            snapshotCamera.transform.SetPositionAndRotation(snapshotPos + Vector3.up * 2,Quaternion.Euler(90, 0, 0));
            snapshotCamera.gameObject.SetActive(true);
            GameObject gameObject = this.newGameObject(0,objectMaterial);   // put in default layer
            Bounds bounds = gameObject.GetComponent<MeshFilter>().mesh.bounds;
            
            RenderTexture rt = new RenderTexture(resWidth, resHeight, 24);
            snapshotCamera.targetTexture = rt;
            float maxsize = bounds.size.x;
            if (maxsize < bounds.size.y) {
                maxsize = bounds.size.y;
            }
            float iconscale = 2f / maxsize;
            
            gameObject.transform.localScale = new Vector3(iconscale,iconscale,iconscale);
            gameObject.transform.position = snapshotPos - (this.centroid * iconscale);
            gameObject.transform.RotateAround(snapshotPos,Vector3.right,90);

            this.icon = new Texture2D(resWidth, resHeight, TextureFormat.RGB24, false);
            snapshotCamera.Render();
            RenderTexture.active = rt;
            this.icon.ReadPixels(new Rect(0, 0, resWidth, resHeight), 0, 0);
            this.icon.Compress(true);
            snapshotCamera.targetTexture = null;
            RenderTexture.active = null; // JC: added to avoid errors
            RenderTexture.Destroy(rt);
            snapshotCamera.gameObject.SetActive(false);
            gameObject.SetActive(false);
            GameObject.Destroy(gameObject);
        }
        return this.icon;
    }

    public GameObject newGameObject(int objectLayer,Material material) {
        
        GameObject gameObject = new GameObject(this.name + "-" + instanceCounter.ToString("D3"),typeof(MeshFilter),typeof(MeshRenderer),typeof(MeshCollider));
        gameObject.GetComponent<MeshFilter>().mesh = mesh;
        gameObject.GetComponent<MeshCollider>().sharedMesh = mesh;
        gameObject.GetComponent<MeshRenderer>().material = material;
        gameObject.layer = objectLayer;
        
        foreach(ConnectorItem connector in this.connectors) {
            connector.newGameObject(gameObject.name).transform.SetParent(gameObject.transform);
        }
        this.instanceCounter++;
        return gameObject;
    }
}
