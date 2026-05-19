using UnityEngine;
using UnityEngine.InputSystem;

public class GameInput : MonoBehaviour
{
    // generate c# class
    private PlayerInputActions playerInputActions;
        
    private void Awake()
    {
        // instantiate object
        playerInputActions = new PlayerInputActions();
        
        // activate the Player action map
        playerInputActions.Player.Enable();
    }
    
    // reads and returns player movement vector as a normalized direction vector
    public Vector2 GetMovementVectorNormalized()
    {
        // gets raw 2D player movement input
        Vector2 inputVector = playerInputActions.Player.Move.ReadValue<Vector2>();
        
        // normalize movement
        inputVector = inputVector.normalized;
        
        return inputVector;
    }
}
