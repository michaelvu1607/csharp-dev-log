using System;
using UnityEngine;
using UnityEngine.InputSystem;

public class GameInput : MonoBehaviour
{
    // broadcast tower for when the Interact button is pressed
    public event EventHandler OnInteractAction;
    
    // generate c# class
    private PlayerInputActions playerInputActions;
        
    private void Awake()
    {
        // instantiate object
        playerInputActions = new PlayerInputActions();
        
        // activate the Player action map
        playerInputActions.Player.Enable();
        
        // connecting local method to Unity's hardware listener
        playerInputActions.Player.Interact.performed += Interact_performed;
    }

    private void Interact_performed(UnityEngine.InputSystem.InputAction.CallbackContext obj)
    {
        // event fired when Interact button is pressed
        OnInteractAction?.Invoke(this, EventArgs.Empty);
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
