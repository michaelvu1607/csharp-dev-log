using System;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{

    [SerializeField] private Vector3 playerVelocity;
    [SerializeField] private float speed = 5f;
    private const float gravity = -9.81f;
    private bool isGrounded;
    private bool isBlocked;
    private Vector3 moveDirection;
    private Vector3 horizontalVelocity;
    private float jumpHeight = 1f;
    private float playerHeight = 2f;
    private float playerRadius = 0.5f;

    void Start()
    {
        
    }

    void Update()
    {
        Vector3 p1 = transform.position + Vector3.up * playerRadius;
        Vector3 p2 = transform.position + Vector3.up * (playerHeight - playerRadius);
        isBlocked = Physics.CapsuleCast(p1, p2, playerRadius, moveDirection,out RaycastHit hit, playerRadius);
        isGrounded = Physics.CapsuleCast(p1, p2, playerRadius, Vector3.down, out RaycastHit hit2, playerHeight / 2);
    }

    public void ProcessMovement(Vector2 input)
    {
        if (!isBlocked)
        {
            moveDirection = new Vector3(input.x, 0f, input.y);
            moveDirection = moveDirection.normalized;
            horizontalVelocity = transform.TransformDirection(moveDirection) * speed;
        }
        else
        {
            horizontalVelocity = Vector3.zero;
        }

        if (!isGrounded)
        {
            playerVelocity.y += gravity * Time.deltaTime;
        }
        else
        {
            if (playerVelocity.y < 0f)
            {
                playerVelocity.y = 0f;
            }
        }
        
        Vector3 finalVelocity = new Vector3(horizontalVelocity.x, playerVelocity.y, horizontalVelocity.z);
        
        transform.position += finalVelocity * Time.deltaTime;
    }

    public void ProcessJump()
    {
        Debug.Log(isGrounded);
        if (isGrounded)
        {
            playerVelocity.y = Mathf.Sqrt(jumpHeight * -3f * gravity);
        }
    }
}
