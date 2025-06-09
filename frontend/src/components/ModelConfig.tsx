
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Plus, Trash2 } from "lucide-react";

type Agent = {
  id: string;
  name: string;
  model: string;
  apiKey: string;
};

const MODEL_OPTIONS = [
  { value: "gpt4", label: "GPT-4" },
  { value: "gpt3", label: "GPT-3.5" },
  { value: "claude", label: "Claude" },
];

const DEFAULT_AGENTS: Agent[] = [
  { id: "research", name: "Research Agent", model: "", apiKey: "" },
  { id: "writing", name: "Writing Agent", model: "", apiKey: "" },
  { id: "review", name: "Review Agent", model: "", apiKey: "" },
];

const ModelConfig = () => {
  const [agents, setAgents] = useState<Agent[]>(DEFAULT_AGENTS);
  const { toast } = useToast();

  const handleModelChange = (agentId: string, model: string) => {
    setAgents(agents.map(agent => 
      agent.id === agentId ? { ...agent, model } : agent
    ));
  };

  const handleApiKeyChange = (agentId: string, apiKey: string) => {
    setAgents(agents.map(agent => 
      agent.id === agentId ? { ...agent, apiKey } : agent
    ));
  };

  const handleAddAgent = () => {
    const newAgent: Agent = {
      id: `agent-${agents.length + 1}`,
      name: `Custom Agent ${agents.length + 1}`,
      model: "",
      apiKey: "",
    };
    setAgents([...agents, newAgent]);
  };

  const handleRemoveAgent = (agentId: string) => {
    setAgents(agents.filter(agent => agent.id !== agentId));
  };

  const handleSave = () => {
    // TODO: Implement actual saving logic
    toast({
      title: "Settings saved",
      description: "Your agent configurations have been updated",
    });
  };

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h2 className="text-lg font-semibold">Agent Configuration</h2>
        <p className="text-sm text-muted-foreground">
          Configure AI models and API settings for each agent
        </p>
      </div>

      <div className="space-y-4">
        {agents.map((agent) => (
          <Card key={agent.id}>
            <CardHeader className="pb-4">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>{agent.name}</CardTitle>
                  <CardDescription>Configure model and API key</CardDescription>
                </div>
                {agents.length > 1 && (
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleRemoveAgent(agent.id)}
                  >
                    <Trash2 className="h-4 w-4 text-muted-foreground" />
                  </Button>
                )}
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor={`model-${agent.id}`}>Model Selection</Label>
                <Select
                  value={agent.model}
                  onValueChange={(value) => handleModelChange(agent.id, value)}
                >
                  <SelectTrigger id={`model-${agent.id}`}>
                    <SelectValue placeholder="Select a model" />
                  </SelectTrigger>
                  <SelectContent>
                    {MODEL_OPTIONS.map((option) => (
                      <SelectItem key={option.value} value={option.value}>
                        {option.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor={`apiKey-${agent.id}`}>API Key</Label>
                <Input
                  id={`apiKey-${agent.id}`}
                  type="password"
                  placeholder="Enter API key"
                  value={agent.apiKey}
                  onChange={(e) => handleApiKeyChange(agent.id, e.target.value)}
                  className="font-mono"
                />
              </div>
            </CardContent>
          </Card>
        ))}

        <Button
          variant="outline"
          className="w-full"
          onClick={handleAddAgent}
        >
          <Plus className="h-4 w-4 mr-2" />
          Add Agent
        </Button>

        <Button onClick={handleSave} className="w-full">
          Save Configuration
        </Button>
      </div>
    </div>
  );
};

export default ModelConfig;
