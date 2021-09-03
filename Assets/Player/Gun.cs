using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class Gun : MonoBehaviour
{
    Transform cam;

    [SerializeField] float range = 50f;
    [SerializeField] GameObject inventory;
    [SerializeField] private Material objectMaterial;
    

    private void Awake()
    {
        cam = Camera.main.transform;
    }

    public void Shoot()
    {
        RaycastHit hit;
        int layerMask = 1 << 8;
        Debug.DrawRay(cam.position,cam.forward * range,Color.green,10.0f);
        Debug.Log("Shoot");
        if (Physics.Raycast(cam.position,cam.forward, out hit,range,layerMask)) {
            print(hit.point);
            print(hit.normal);
            print(hit.transform.name);
        }
    }

    public void Insert() {
        inventory.SetActive(true);
        Time.timeScale = 0f;
    }
    public void Delete() {
        if (this.transform.childCount == 1) {
            Destroy(this.transform.GetChild(0).transform.gameObject);
        }
    }
    
    public void equip(string name) {
        GameObject go = Library.newGameobject(name,0.5f);
        
        go.transform.SetParent(this.transform,false);

        Time.timeScale = 1f;
    }
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
