"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { loginUser } from "@/lib/api";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import Link from "next/link";

export default function LoginPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const router = useRouter();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const formData = new FormData();
            formData.append("username", email);
            formData.append("password", password);

            const data = await loginUser(formData);
            localStorage.setItem("token", data.access_token);

            toast.success("Welcome back!", {
                description: "Logged in successfully."
            });
            router.push("/");
        } catch (error) {
            toast.error("Login Failed", {
                description: "Invalid credentials."
            });
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <Card className="w-full max-w-md">
                <CardHeader>
                    <CardTitle className="text-center">Admin Login</CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleLogin} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="email">Email</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="admin@hemut.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="password">Password</Label>
                            <Input
                                id="password"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                        </div>
                        <Button type="submit" className="w-full">Sign In</Button>
                        <div className="text-center text-sm text-muted-foreground mt-4">
                            Don't have an account?{" "}
                            <Link href="/register" className="text-blue-600 hover:underline">
                                Register here
                            </Link>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}