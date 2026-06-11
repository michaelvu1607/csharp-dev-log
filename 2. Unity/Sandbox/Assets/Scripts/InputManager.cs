using System;
using UnityEngine;
using UnityEngine.InputSystem;

public class InputManager : MonoBehaviour
{
    private PlayerInputActions playerInputActions;
    private PlayerInputActions.PlayerActions playerActions;
    private PlayerMovement playerMovement;
    private PlayerLook playerLook;
    void Awake()
    {
        playerInputActions = new PlayerInputActions();
        playerActions = playerInputActions.Player;
        playerMovement = GetComponent<PlayerMovement>();
        playerLook = GetComponent<PlayerLook>();
        playerActions.Jump.performed += ctx => playerMovement.ProcessJump();
    }

    void FixedUpdate()
    {
        playerMovement.ProcessMovement(playerActions.Movement.ReadValue<Vector2>());
    }

    private void LateUpdate()
    {
        playerLook.ProcessLook(playerActions.Look.ReadValue<Vector2>());
    }
    
    void OnEnable()
    {
        playerActions.Enable();
    }
    
    void OnDisable()
    {
        playerActions.Disable();
    }
}
