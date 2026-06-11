using UnityEngine;

public class PlayerLook : MonoBehaviour
{
    public Camera cam;
    private float xRotation = 0f;

    public float xSensitivity = 10f;
    public float ySensitivity = 10f;
    
    public void ProcessLook(Vector2 input)
    {
        float mouseX = input.x;
        float mouseY = input.y;
        
        xRotation -= mouseY * ySensitivity * Time.deltaTime;
        xRotation = Mathf.Clamp(xRotation, -90f, 90f);
        cam.transform.localRotation = Quaternion.Euler(xRotation, 0f, 0f);
        transform.Rotate(Vector3.up, mouseX * xSensitivity * Time.deltaTime);
    }
}
