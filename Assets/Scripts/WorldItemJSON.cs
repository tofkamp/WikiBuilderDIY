using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WorldItemJSON
{
    public string name;
    public float x,y,z;
    public float eulerX,eulerY,eulerZ;

    public WorldItemJSON() {
        this.name = "";
        this.x = 0;
        this.y = 0;
        this.z = 0;
        this.eulerX = 0;
        this.eulerY = 0;
        this.eulerZ = 0;
    }
    
    public WorldItemJSON(GameObject gameObject) {
    //     string nameInstance = gameObject.GetComponent<MeshFilter>().mesh.name;  // name is added with " Instance"
    //     this.name = nameInstance.Substring(0,nameInstance.Length - 9);
        this.name = gameObject.GetComponent<MeshCollider>().sharedMesh.name;
        this.x = (float) System.Math.Round(gameObject.transform.position.x,3);
        this.y = (float) System.Math.Round(gameObject.transform.position.y,3);
        this.z = (float) System.Math.Round(gameObject.transform.position.z,3);
        Vector3 eulerAngles = gameObject.transform.eulerAngles;
        this.eulerX = (float) System.Math.Round(eulerAngles.x,3);
        this.eulerY = (float) System.Math.Round(eulerAngles.y,3);
        this.eulerZ = (float) System.Math.Round(eulerAngles.z,3);
    }
    public Vector3 GetPosition() {
        return new Vector3(this.x, this.y, this.z);
    }
    public Quaternion GetRotation() {
        Quaternion rotation = new Quaternion();
        rotation.eulerAngles = new Vector3(this.eulerX, this.eulerY, this.eulerZ);
        return rotation;
    }
}
