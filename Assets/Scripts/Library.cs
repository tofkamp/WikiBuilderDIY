using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;
using System.IO;

public static class Library
{
    /*#region Singleton

    public static Library instance;

	void Awake ()
	{
		if (instance != null)
		{
			Debug.LogWarning("More than one library of Inventory found!");
			return;
		}

		instance = this;
	}

	#endregion
*/

    public static List<LibraryItem> libraryItems = new List<LibraryItem>();
    private static Material material;
    
    public static void setMaterial(Material mat) {
        material = mat;
    }
    public static void Load(string fullPath) {
        //Load Data
        //string fullPath = Application.persistentDataPath + directory + filename;

        //assert File.Exists(fullPath),"Libraryfile does not exist";
        string jsonFile = File.ReadAllText(fullPath);
        List<LibraryItemJSON> jsonlibrary = JsonConvert.DeserializeObject<List<LibraryItemJSON>>(jsonFile);
        
        foreach(LibraryItemJSON libjson in jsonlibrary) {
            libraryItems.Add(new LibraryItem(libjson));
        }
    }

    public static GameObject newGameobject(string name,float scaledto = 0) {
        foreach(LibraryItem libitem in Library.libraryItems) {
            if (name == libitem.name) {
                GameObject gameObject = libitem.newGameObject(8,material);
                if (scaledto != 0) {
                    Bounds bounds = gameObject.GetComponent<MeshFilter>().mesh.bounds;
                    float maxsize = bounds.size.x;
                    if (maxsize < bounds.size.y) {
                        maxsize = bounds.size.y;
                    }
                    float iconscale = scaledto / maxsize;
                    
                    gameObject.transform.localScale = new Vector3(iconscale,iconscale,iconscale);
                    gameObject.transform.position = -libitem.centroid * iconscale;
                }
                return gameObject;
            }
        }
        return null;
    }
}
