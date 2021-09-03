using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ConnectorItem {
    private Vector3 centroid;
    private string type;
    private Vector3 scale;
    private float rotateZ;
    private int connectornr;


    public ConnectorItem(ConnectorItemJSON conjson,int connectornr) {
        const float scale = 1000f;
        this.centroid = new Vector3(conjson.centroid[0] ,conjson.centroid[1], conjson.centroid[2]) / scale;
        // replace previous line with this to have connectors besides shape
        //this.centroid = new Vector3(conjson.centroid[0] ,conjson.centroid[1], conjson.centroid[2] + 18) / scale;
        this.type = conjson.type;
        this.connectornr = connectornr;
        if (conjson.widthX < conjson.heightY) {
            this.rotateZ = conjson.rotateZ;
            this.scale = new Vector3(conjson.heightY, conjson.widthX, conjson.depthZ) / (scale - 100);
        } else {
            this.rotateZ = 90 + conjson.rotateZ;
            this.scale = new Vector3(conjson.widthX, conjson.heightY, conjson.depthZ) / scale;
        }
    }

    public GameObject newGameObject(string libraryItemId) {
        
        GameObject gameObject = GameObject.CreatePrimitive(PrimitiveType.Cube);
        gameObject.name = libraryItemId + "#" + this.connectornr.ToString("D02") + "-" + this.type;
        gameObject.transform.Translate(this.centroid);
        gameObject.transform.eulerAngles = new Vector3(0,0,this.rotateZ);
        gameObject.transform.localScale = this.scale;
        gameObject.layer = 9;
        gameObject.GetComponent<Renderer>().material.color = Color.red;
        return gameObject;
    }
}
