using System.Collections;
using System.Collections.Generic;
using UnityEngine.EventSystems;
using UnityEngine;

public class InputManager : MonoBehaviour
{
    [SerializeField] Movement movement;
    [SerializeField] MouseLook mouseLook;
    [SerializeField] Gun gun;
    [SerializeField] Material objectMaterial;
    [SerializeField] World world;

    //[SerializeField] private Library library;
    
    PlayerControls controls;
    PlayerControls.GroundMovementActions groundMovement;

    Vector2 horizontalInput;
    Vector2 mouseInput;
    Vector2 rotationInput;


    private void Awake() {
        controls = new PlayerControls();
        groundMovement = controls.GroundMovement;

        // groundMovement.[action].performed += context => do something
        groundMovement.HorizontalMovement.performed += ctx => horizontalInput = ctx.ReadValue<Vector2>();
        
        groundMovement.MouseX.performed += ctx => mouseInput.x = ctx.ReadValue<float>();
        groundMovement.MouseY.performed += ctx => mouseInput.y = ctx.ReadValue<float>();

        groundMovement.Shoot.performed += _ => gun.Shoot();
        groundMovement.Rotate.performed += ctx => rotationInput = ctx.ReadValue<Vector2>();
        groundMovement.Inventory.performed += _ => gun.Insert();
        groundMovement.Delete.performed += _ => gun.Delete();
        //groundMovement.Select.performed += _ => gun.Select();
        groundMovement.Exit.performed += _ => movement.Exit();
    }

    private void OnEnable() {
        controls.Enable();
    }

    private void OnDestroy() {
        controls.Disable();
    }
        
    
    // Start is called before the first frame update
    void Start()
    {
        //GameObject trede = Library.newGameobject("trede");
        // set scale
        // set layer naar default
        // set center
        //trede.transform.SetParent(gun.transform,false);
        gun.equip("trede");
    }

    // Update is called once per frame
    void Update()
    {
        if (EventSystem.current.IsPointerOverGameObject()) {
            return;
        }
        movement.ReceiveInput(horizontalInput);
        mouseLook.ReceiveInput(mouseInput);
    }
}
