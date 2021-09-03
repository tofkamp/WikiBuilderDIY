using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Movement : MonoBehaviour
{
    [SerializeField] CharacterController controller;
    [SerializeField] float speed = 8f;
    Vector2 horizontalInput;

    public void ReceiveInput(Vector2 _horizontalInput)
    {
        horizontalInput = _horizontalInput;
        //print(horizontalInput);
    }
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        Vector3 horizontalVelocity = (transform.right * horizontalInput.x + transform.forward * horizontalInput.y) * speed;
        controller.Move(horizontalVelocity * Time.deltaTime);
    }

    public void Exit()
    {
        Debug.Log("exit naar main menu");
        Application.Quit();
    }
}
