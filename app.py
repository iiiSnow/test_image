import gradio as gr
import torch
from torchvision import transforms

torch.hub._validate_not_a_forked_repo=lambda a,b,c: True
model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet18', pretrained=True).eval()

# 读取本地文件内容
with open("xx.txt", "r") as file:
    labels = file.read().split("\n")

def predict(inp):
  inp = transforms.ToTensor()(inp).unsqueeze(0)
  with torch.no_grad():
    prediction = torch.nn.functional.softmax(model(inp)[0], dim=0)
    confidences = {labels[i]: float(prediction[i]) for i in range(1000)}
  return confidences

demo = gr.Interface(fn=predict, 
             inputs=gr.inputs.Image(type="pil"),
             outputs=gr.outputs.Label(num_top_classes=3),
             examples=[["cheetah.jpg"]],
             )
             
demo.launch()
