using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using Newtonsoft.Json;
using System.IO;

/* wat hebben we nog nodig
panels
- disclaimer
- start scherm
  - tutorial
  - help
  - resume
  - newgame
    - newgame name
  - load game
  - save game
  - export .OBJ
  - options
  - quit
- Library item picker

optional
- rotate light

to do:
split world en player controller

*/
public class World : MonoBehaviour
{
    [SerializeField] private Material objectMaterial;
    [SerializeField] private Camera snapshotCamera;
//    public Library library = new Library();

    //private GameObject sourceConnector,targetConnector;
    private GameObject world;
    [SerializeField] private GameObject inventory;
    
    // Start is called before the first frame update
    void Start()
    {
        Application.targetFrameRate = 30;
        world = GameObject.Find("/World");
        const string FullPath = "C:/Users/Tjibbe/OneDrive/python/Polygon/Library/ladder.json";
        Library.Load(FullPath);
        Library.setMaterial(objectMaterial);
        //sourceConnector = GameObject.Find("midsteun-001#00-18x18x60");
        //targetConnector = GameObject.Find("a-000#01-18x18x60");
        //sourceConnector.transform.parent.transform.Rotate(Random.Range(-5f,+5f),Random.Range(-5f,+5f),Random.Range(-5f,+5f));
        
        //save("world.json");
        load("world.json");
        //int resWidth = 128;
        //int resHeight = 128;
        //GameObject inventory = GameObject.Find("/Canvas/Inventory");
        foreach(LibraryItem libitem in Library.libraryItems) {
            //Texture2D icon = libitem.getIcon(snapshotCamera, objectMaterial);
            GameObject gameObject = new GameObject(libitem.name,typeof(RawImage),typeof(Button));
            gameObject.transform.SetParent(inventory.transform);
            RawImage icon = gameObject.GetComponent<RawImage>();
            icon.texture = libitem.getIcon(snapshotCamera, objectMaterial);
            //icon.raycastTarget = false;
            Button button = gameObject.GetComponent<Button>();
            button.onClick.AddListener(() => TaskWithParameters(libitem.name));
            ColorBlock kleur = ColorBlock.defaultColorBlock;
            kleur.highlightedColor =  new Color(1f, 1f, 1f, 0.5f);
            button.colors = kleur;
            /*byte[] bytes = screenShot.EncodeToPNG();
            string filename = string.Format("{0}/screenshots/{4}_{1}x{2}_{3}.png", 
                              Application.dataPath, 
                              resWidth, resHeight, 0,
                              //System.DateTime.Now.ToString("yyyy-MM-dd_HH-mm-ss"),
                              libitem.name); */
            //System.IO.File.WriteAllBytes(filename, bytes);
            //Debug.Log(string.Format("Took screenshot to: {0}", filename));
            //break;
            //gameObject.transform.Translate(0,0,-2 - nr);
            //nr++;
            //gameObject.SetActive(false);
            //Destroy(gameObject);
        }
        snapshotCamera.gameObject.SetActive(false);
    }
    void TaskWithParameters(string message)
    {
        //Output this to console when the Button2 is clicked
        Debug.Log(message);
    }
    private bool connect(float maxAngle, GameObject sourceConnector,GameObject targetConnector) {
        bool withinlimits = false;
        // check if connectors are the same type
        if (sourceConnector.transform.localScale != targetConnector.transform.localScale) {
            return withinlimits;
        }
        // convert connector x direction to world, and back to local space of the parent of the sourceConnector
        Vector3 sourceDirection = sourceConnector.transform.parent.transform.InverseTransformVector(transform.TransformVector(sourceConnector.transform.right));
        Vector3 targetDirection = sourceConnector.transform.parent.transform.InverseTransformVector(transform.TransformVector(targetConnector.transform.right));

        float angle = Vector3.Angle(targetDirection,sourceDirection);
        //Debug.Log("Right " + angle.ToString());
        if (angle < maxAngle) {
            Quaternion rot = Quaternion.FromToRotation(sourceDirection, targetDirection);
            sourceConnector.transform.parent.transform.rotation *= rot;
            withinlimits = true;
        }
        if (angle > 180 - maxAngle) {  // right was left, so inverse direction
            Quaternion rot = Quaternion.FromToRotation(sourceDirection, -targetDirection);
            sourceConnector.transform.parent.transform.rotation *= rot;
            withinlimits = true;
        }
        
        if (withinlimits) {
            // if x-right angle is within limits, check for rotation needed in z axis. Rotate to y-axis (up).
            // 
            withinlimits = false;
            // convert connector y direction to world, and back to local space of the parent of the sourceConnector
            sourceDirection = sourceConnector.transform.parent.transform.InverseTransformVector(transform.TransformVector(sourceConnector.transform.up));
            targetDirection = sourceConnector.transform.parent.transform.InverseTransformVector(transform.TransformVector(targetConnector.transform.up));
            angle = Vector3.Angle(targetDirection,sourceDirection);
            //Debug.Log("Up " + angle.ToString());
            if (angle < maxAngle) {
                Quaternion rot = Quaternion.FromToRotation(sourceDirection, targetDirection);
                sourceConnector.transform.parent.transform.rotation *= rot;
                withinlimits = true;
            }
            if (angle > 180 - maxAngle) {        // is it down instead ?
                Quaternion rot = Quaternion.FromToRotation(sourceDirection, -targetDirection);
                sourceConnector.transform.parent.transform.rotation *= rot;
                withinlimits = true;
            }
            // Also 90 degrees are possible, rotate to z-axis (forward)
            if (angle > 90 - maxAngle && angle < 90 + maxAngle && sourceConnector.transform.localScale.y == targetConnector.transform.localScale.z) {
                sourceDirection = sourceConnector.transform.parent.transform.InverseTransformVector(transform.TransformVector(sourceConnector.transform.forward));
                // targetDirection is already calculated
                angle = Vector3.Angle(targetDirection,sourceDirection);
                //Debug.Log("Forward " + angle.ToString());
                if (angle < maxAngle) {
                    Quaternion rot = Quaternion.FromToRotation(sourceDirection, targetDirection);
                    sourceConnector.transform.parent.transform.rotation *= rot;
                    withinlimits = true;
                }
                if (angle > 180 - maxAngle) {      // backwards
                    Quaternion rot = Quaternion.FromToRotation(sourceDirection, -targetDirection);
                    sourceConnector.transform.parent.transform.rotation *= rot;
                    withinlimits = true;
                }
                
            }
            //sourceConnector.transform.parent.transform.Translate(targetPosition - sourceConnector.transform.position);
            //  https://gamedevelopment.tutsplus.com/tutorials/bake-your-own-3d-dungeons-with-procedural-recipes--gamedev-14360
            //  https://forum.unity.com/threads/rotate-an-object-so-its-child-matches-another-objects-child-rotation.511730/
            // 
            if (withinlimits) {
                // if rotation is possible, calculate new position in order both connectors are on the same position
                Vector3 sourcePosition = transform.TransformPoint(sourceConnector.transform.position);
                Vector3 targetPosition = transform.TransformPoint(targetConnector.transform.position);
                sourceConnector.transform.parent.transform.position = targetPosition - (sourceConnector.transform.position - sourceConnector.transform.parent.transform.position);
            }
        }
        return withinlimits;
    }

    public void save(string filename) {
        List<WorldItemJSON> worldItems = new List<WorldItemJSON>();
        foreach (Transform child in world.transform) {
            worldItems.Add(new WorldItemJSON(child.gameObject));
        }
        // http://www.newtonsoft.com/json/help/html/SerializingJSON.htm
        string worldItemsinJSON = JsonConvert.SerializeObject(worldItems,Formatting.Indented );
        System.IO.File.WriteAllText(Application.persistentDataPath + '/' + filename, worldItemsinJSON);
        Debug.Log(Application.persistentDataPath + '/' + filename);
    }
    public bool load(string filename) {
        /// load world from a json file
        /// return false if it failes
        string jsonFile = File.ReadAllText(Application.persistentDataPath + '/' + filename);
        List<WorldItemJSON> worldItems = JsonConvert.DeserializeObject<List<WorldItemJSON>>(jsonFile);
        foreach(WorldItemJSON item in worldItems) {
            GameObject gameObject = Library.newGameobject(item.name);
            gameObject.transform.SetParent(world.transform);
            gameObject.transform.SetPositionAndRotation(item.GetPosition(),item.GetRotation());
        }
        return true;
    }
    public void clear() {
        /// <summary>
        /// Clear all object from the world
        /// </summary>
        /// <value></value>
        foreach (Transform child in world.transform) {
            child.gameObject.SetActive(false);
            Destroy(child.gameObject);
        }
    }

    private string enabledConnector = "";
    public void showConnector(string connectorType) {
        if (enabledConnector != connectorType) {
            foreach (Transform child in world.transform) {
                foreach(Transform childConnector in child.transform) {
                    if (childConnector.gameObject.name.EndsWith(connectorType)) {
                        childConnector.gameObject.SetActive(true);
                    } else {
                        childConnector.gameObject.SetActive(false);
                    }
                }
            }
            enabledConnector = connectorType;
        }
        Camera.main.cullingMask = Physics.AllLayers;
    }
    public void noshowConnector() {
        Camera.main.cullingMask = Physics.AllLayers ^ (1 << 9);    // show everything except connectors
    }
}
