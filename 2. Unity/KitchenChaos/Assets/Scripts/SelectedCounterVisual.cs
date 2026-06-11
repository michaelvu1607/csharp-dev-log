using UnityEngine;

// each clearCounter contains this script
public class SelectedCounterVisual : MonoBehaviour
{
    // specific counter this script is attached to
    [SerializeField] private BaseCounter baseCounter;
    
    // visual mesh turned on and off
    [SerializeField] private GameObject[] visualGameObjectArray;
    private void Start()
    {
        // uses Singleton to find Player and then subscribes
        Player.Instance.OnSelectedCounterChanged += Player_OnSelectedCounterChanged;
    }

    // executes immediately after Player looks at a different counter
    private void Player_OnSelectedCounterChanged(object sender, Player.OnSelectedCounterChangedEventArgs e)
    {
        // checks if counter Player is looking at matches this counter
        if (e.selectedCounter == baseCounter)
        {
            Show();
        }
        else
        {
            Hide();
        }
    }

    private void Show()
    {
        foreach (GameObject go in visualGameObjectArray)
            go.SetActive(true);
    }
    private void Hide()
    {
        foreach (GameObject go in visualGameObjectArray)
            go.SetActive(false);
    }
}
